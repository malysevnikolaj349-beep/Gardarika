import asyncio
import time
import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add root to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))

# Mock environment variable before importing bot to avoid print errors
with patch.dict(os.environ, {"TELEGRAM_TOKEN": "dummy"}):
    import bot


class TestBotAsync(unittest.IsolatedAsyncioTestCase):
    async def test_start_handler_concurrency(self):
        # Mock the database operation to be slow (blocking)
        # We patch 'bot.add_user_if_not_exists' because bot.py imports it
        # directly
        with patch('bot.add_user_if_not_exists') as mock_db:
            # Simulate a blocking I/O operation
            def blocking_op(*args, **kwargs):
                time.sleep(0.5)

            mock_db.side_effect = blocking_op

            # Mock update and context
            mock_update = MagicMock()
            mock_update.effective_user.id = 123
            mock_update.effective_user.mention_html.return_value = "User"
            # reply_html must be awaitable
            mock_update.message.reply_html = MagicMock(
                return_value=asyncio.Future()
            )
            mock_update.message.reply_html.return_value.set_result(None)

            mock_context = MagicMock()

            print("Running handlers concurrently...")
            start_time = time.time()

            # Run two handlers concurrently
            await asyncio.gather(
                bot.start(mock_update, mock_context),
                bot.start(mock_update, mock_context)
            )

            end_time = time.time()
            duration = end_time - start_time
            print(f"Total duration: {duration:.2f}s")

            # If blocking, it should take at least 0.5 * 2 = 1.0s
            # If async/threaded, it should take approx 0.5s

            # Now we expect it to be ASYNC/THREADED (fast)
            self.assertLess(
                duration, 0.6,
                "Handlers ran sequentially, expected parallel execution"
            )


if __name__ == "__main__":
    unittest.main()
