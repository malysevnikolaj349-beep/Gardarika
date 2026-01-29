import sys
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

# Insert root directory to sys.path to allow importing bot
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, ROOT_DIR)

# Clear gardarika from sys.modules if it was loaded from src
# This ensures bot.py imports gardarika from root (where database/ exists)
keys_to_remove = [k for k in sys.modules if k.startswith('gardarika')]
for k in keys_to_remove:
    del sys.modules[k]

try:
    from bot import start, profile, create_character_start
except ImportError:
    # Fallback if imports fail due to structure
    pass

@pytest.mark.asyncio
async def test_start_handler_async_db():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "@testuser"
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # We want to verify that add_user_if_not_exists is called via asyncio.to_thread
    with patch('bot.add_user_if_not_exists') as mock_db_call:
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            await start(update, context)

            # Verify asyncio.to_thread was called with the DB function
            mock_to_thread.assert_called_with(mock_db_call, user.id)

            # Verify reply was sent
            update.message.reply_html.assert_called_once()

@pytest.mark.asyncio
async def test_profile_handler_async_db():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    mock_char = {
        'name': 'Hero',
        'class_name': 'Warrior',
        'faction_name': 'Faction',
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

    with patch('bot.get_character_by_user_id') as mock_db_call:
        # Mocking the return value of asyncio.to_thread to return mock_char
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            mock_to_thread.return_value = mock_char

            await profile(update, context)

            # Verify asyncio.to_thread was called with the DB function
            mock_to_thread.assert_called_with(mock_db_call, user.id)

            # Verify reply was sent
            update.message.reply_html.assert_called_once()

@pytest.mark.asyncio
async def test_create_character_start_async_db():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_text = AsyncMock()

    with patch('bot.get_character_by_user_id') as mock_db_call:
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            # Case where user already has character
            mock_to_thread.return_value = {'some': 'data'}

            from telegram.ext import ConversationHandler

            result = await create_character_start(update, context)

            mock_to_thread.assert_called_with(mock_db_call, user.id)
            assert result == ConversationHandler.END
