import asyncio
import time
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Ensure root is in path
sys.path.insert(0, os.path.abspath("."))

# Import the handlers from bot
# Note: This requires the gardarika package to be available in path
from bot import profile, start

@pytest.mark.asyncio
async def test_profile_handler_concurrency():
    """
    Verifies whether the profile handler blocks the event loop during database operations.
    """
    # Mock update and context
    update = MagicMock()
    update.effective_user.id = 123

    # Mock reply_html to be an async function (awaitable)
    async def async_reply(*args, **kwargs):
        pass
    update.message.reply_html = MagicMock(side_effect=async_reply)
    update.message.reply_text = MagicMock(side_effect=async_reply)

    context = MagicMock()

    # Mock data
    mock_char_data = {
        'name': 'Test', 'class_name': 'Warrior', 'faction_name': 'Kiev',
        'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
        'strength': 10, 'dexterity': 10, 'wisdom': 10, 'endurance': 10, 'charisma': 10
    }

    # Define a blocking side effect
    def blocking_db_call(*args):
        time.sleep(0.2) # Block for 200ms
        return mock_char_data

    # Setup the background task to measure loop responsiveness
    ticks = []
    async def ticker():
        try:
            while True:
                ticks.append(time.time())
                await asyncio.sleep(0.02) # Tick every 20ms
        except asyncio.CancelledError:
            pass

    # Patch the database function used in bot.py
    # We patch 'bot.get_character_by_user_id' because bot.py imports it.
    with patch('bot.get_character_by_user_id', side_effect=blocking_db_call):

        # Start ticker
        ticker_task = asyncio.create_task(ticker())

        # Run the handler
        start_time = time.time()
        await profile(update, context)
        end_time = time.time()

        # Stop ticker
        ticker_task.cancel()
        try:
            await ticker_task
        except asyncio.CancelledError:
            pass

    total_time = end_time - start_time
    num_ticks = len(ticks)

    print(f"\nTotal execution time: {total_time:.4f}s")
    print(f"Loop ticks during execution: {num_ticks}")

    # Expected behavior:
    # If blocking: time.sleep(0.2) blocks the loop. The ticker (sleep 0.02) cannot run.
    # We might get 0 or 1 tick (the one before or after).
    # Expected ticks if non-blocking: 0.2 / 0.02 = ~10 ticks.

    # We assert that we have verified the behavior.
    # For now, I'll just fail if it's blocking so we can see the "red" test.
    # If num_ticks < 5, it's blocking.

    assert num_ticks >= 5, f"Event loop was blocked! Only {num_ticks} ticks occurred during 0.2s operation."
