import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Hack to handle collision between src/gardarika and root gardarika
if 'gardarika' in sys.modules:
    # If the loaded gardarika is not the root one (has 'src' in path), unload
    # We can check __file__ or __path__
    module = sys.modules['gardarika']
    if hasattr(module, '__path__') and any('src' in p for p in module.__path__):
        del sys.modules['gardarika']
        # Also unload submodules
        for key in list(sys.modules.keys()):
            if key.startswith("gardarika."):
                del sys.modules[key]

# Ensure root is in path
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

import bot


@pytest.mark.asyncio
async def test_start_async_db_call():
    """
    Test that start handler calls add_user_if_not_exists via asyncio.to_thread.
    """
    # Mock update and context
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "User"
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    context = MagicMock()

    # Mock the DB function imported in bot
    with patch('bot.add_user_if_not_exists') as mock_db:
        # Mock asyncio.to_thread to verify it's used
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            # We want to_thread to actually call the function
            # (or just return what we expect)
            # Since add_user returns None, we can just let it be.

            await bot.start(update, context)

            # Verify to_thread was called with our db function and user id
            mock_thread.assert_called_with(mock_db, 12345)


@pytest.mark.asyncio
async def test_profile_async_db_call():
    """
    Test that profile calls get_character_by_user_id via asyncio.to_thread.
    """
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    context = MagicMock()

    # Mock the DB function imported in bot
    with patch('bot.get_character_by_user_id') as mock_db:
        # Mock asyncio.to_thread
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            # Setup return value for to_thread to simulate db return
            mock_thread.return_value = None

            await bot.profile(update, context)

            mock_thread.assert_called_with(mock_db, 12345)
