
import asyncio
import time
import pytest
import sys
import os
from unittest.mock import MagicMock, patch

# Ensure root directory is in sys.path to import bot.py
sys.path.insert(0, os.path.abspath("."))

from bot import start

# Mock update and context
def create_mock_update_context():
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "@user"
    update.effective_user = user
    update.message.reply_html = MagicMock()

    # Make reply_html return a future so it can be awaited
    f = asyncio.Future()
    f.set_result(None)
    update.message.reply_html.return_value = f

    context = MagicMock()
    return update, context

@pytest.mark.asyncio
async def test_start_handler_blocking_behavior():
    # We patch the function imported IN bot.py
    # Note: bot.py does 'from gardarika.database.operations import add_user_if_not_exists'
    # So we must patch 'bot.add_user_if_not_exists'

    with patch("bot.add_user_if_not_exists") as mock_db_op:
        # Simulate blocking I/O: sleep for 0.1 seconds
        def blocking_side_effect(*args, **kwargs):
            time.sleep(0.1)

        mock_db_op.side_effect = blocking_side_effect

        update1, context1 = create_mock_update_context()
        update2, context2 = create_mock_update_context()

        start_time = time.perf_counter()

        # Run two handlers "concurrently"
        await asyncio.gather(
            start(update1, context1),
            start(update2, context2)
        )

        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"Duration: {duration:.4f}s")

        # If blocking (current state): duration >= 0.2s
        # If optimized (future state): duration < 0.15s (overhead allowed)

        assert duration < 0.15, f"Execution was too slow ({duration:.4f}s), indicating blocking calls."
