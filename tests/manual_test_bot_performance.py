import sys
import os
import asyncio
import time
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Add root directory to sys.path to allow importing bot
sys.path.insert(0, os.path.abspath("."))

# Mock environment variable before importing bot
os.environ["TELEGRAM_TOKEN"] = "test_token"

import bot  # noqa: E402


# Mock the blocking database call
def slow_db_call(*args, **kwargs):
    time.sleep(1.0)  # Simulate 1 second blocking DB operation
    return {
        'name': 'TestChar',
        'class_name': 'Warrior',
        'faction_name': 'Kiev',
        'level': 1,
        'experience': 0,
        'health': 100,
        'mana': 50,
        'strength': 10,
        'dexterity': 10,
        'wisdom': 10,
        'endurance': 10,
        'charisma': 10
    }


@pytest.mark.asyncio
async def test_profile_concurrent_performance():
    """
    Verifies that bot.profile handler handles concurrent requests efficiently.

    If the DB call is blocking, two concurrent requests will take sum of their durations.
    If the DB call is async/threaded, they will overlap.
    """

    # Patch the function where it is imported in bot.py
    # Note: bot.py does 'from gardarika.database.operations import get_character_by_user_id'
    # so we must patch 'bot.get_character_by_user_id'
    with patch('bot.get_character_by_user_id', side_effect=slow_db_call):

        # Create two mock updates
        update1 = MagicMock()
        update1.effective_user.id = 123
        update1.message.reply_html = AsyncMock()

        update2 = MagicMock()
        update2.effective_user.id = 456
        update2.message.reply_html = AsyncMock()

        context = MagicMock()

        print("\nStarting concurrent profile requests...")
        start_time = time.time()

        # Run both handlers concurrently
        await asyncio.gather(
            bot.profile(update1, context),
            bot.profile(update2, context)
        )

        end_time = time.time()
        duration = end_time - start_time

        print(f"Total duration: {duration:.2f} seconds")

        # Assertions
        # With blocking calls: duration ~ 2.0s
        # With non-blocking calls: duration ~ 1.0s

        # This test serves as a benchmark.
        # For now, we just print the time. We can add assertion later if we want to enforce it.
        return duration


if __name__ == "__main__":
    # Allow running this script directly
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test_profile_concurrent_performance())
