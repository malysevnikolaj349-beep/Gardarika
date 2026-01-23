import asyncio
import sys
import os
import time
from unittest.mock import MagicMock, patch
import pytest

# Add root to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))

# Now import bot (ignore import error for linter since it's dynamic)
import bot  # noqa: E402

async def heartbeat(counter, stop_event):
    """Increments counter every 0.01s until stop_event is set."""
    while not stop_event.is_set():
        counter['value'] += 1
        await asyncio.sleep(0.01)

def slow_db_call(*args, **kwargs):
    """Simulates a blocking DB call."""
    time.sleep(0.1)

@pytest.mark.asyncio
async def test_start_handler_performance():
    """
    Tests if bot.start handler blocks the event loop.
    """
    # Mock update and context
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "@testuser"
    update.effective_user = user
    update.message.reply_html = MagicMock() # This is async in real lib but we mock return value
    # If reply_html is awaited in bot.py, we need it to return an awaitable or just be a Mock if bot.py doesn't await properly (it does await)
    # MagicMock is not awaitable by default. We need AsyncMock or set return_value to a future.
    # But simpler: make reply_html return a done future.
    f = asyncio.Future()
    f.set_result(None)
    update.message.reply_html.return_value = f

    context = MagicMock()

    # Patch the DB call in bot module
    with patch('bot.add_user_if_not_exists', side_effect=slow_db_call):
        counter = {'value': 0}
        stop_event = asyncio.Event()

        # Start heartbeat task
        monitor_task = asyncio.create_task(heartbeat(counter, stop_event))

        # Run the handler
        # If bot.start calls blocking slow_db_call, the loop freezes,
        # and heartbeat cannot run until slow_db_call finishes.
        await bot.start(update, context)

        # Stop heartbeat
        stop_event.set()
        await monitor_task

        print(f"\nHeartbeats during handler: {counter['value']}")

        # In a blocking scenario, we expect very few heartbeats (maybe 0 or 1).
        # In a non-blocking scenario (0.1s sleep), we expect ~10 heartbeats (0.1 / 0.01).
        return counter['value']
