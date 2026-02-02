import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Setup path to prioritize root directory
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Remove src from path if present to avoid conflict
sys.path = [p for p in sys.path if os.path.abspath(p) != os.path.abspath(SRC_DIR)]

# Ensure root is at the beginning
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Force reload of gardarika modules to ensure we get the root version
keys_to_remove = [k for k in sys.modules if k.startswith('gardarika')]
for k in keys_to_remove:
    del sys.modules[k]

import bot

@pytest.mark.asyncio
async def test_start_uses_to_thread():
    """Test that start handler offloads DB call to thread."""
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.add_user_if_not_exists') as mock_db_op:
            await bot.start(update, context)
            mock_to_thread.assert_awaited_once_with(mock_db_op, 12345)

@pytest.mark.asyncio
async def test_profile_uses_to_thread():
    """Test that profile handler offloads DB call to thread."""
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.get_character_by_user_id') as mock_db_op:
            mock_to_thread.return_value = {
                'name': 'Bolt', 'class_name': 'Rogue', 'faction_name': 'Forest',
                'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
                'strength': 10, 'dexterity': 10, 'wisdom': 10,
                'endurance': 10, 'charisma': 10
            }
            await bot.profile(update, context)
            mock_to_thread.assert_awaited_once_with(mock_db_op, 12345)

@pytest.mark.asyncio
async def test_create_character_start_uses_to_thread():
    """Test that create_character_start handler offloads DB call to thread."""
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.get_character_by_user_id') as mock_db_op:
            mock_to_thread.return_value = None
            await bot.create_character_start(update, context)
            mock_to_thread.assert_awaited_once_with(mock_db_op, 12345)

@pytest.mark.asyncio
async def test_choose_faction_uses_to_thread():
    """Test that choose_faction handler offloads create_character to thread."""
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    update.callback_query.data = 'novgorod'

    context = MagicMock()
    context.user_data = {
        'name': 'Bolt',
        'class': 'охотник',
        'faction': 'novgorod'
    }

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.create_character') as mock_create_char:
            with patch('bot.Character') as mock_character_class:
                mock_char_instance = MagicMock()
                mock_char_instance.name = 'Bolt'
                mock_char_instance.character_class.name = 'Охотник'
                mock_char_instance.faction = {'name': 'Novgorod'}
                mock_char_instance.health = 100
                mock_char_instance.mana = 50
                mock_char_instance.attributes = {}
                mock_character_class.return_value = mock_char_instance

                await bot.choose_faction(update, context)

                assert mock_to_thread.call_args[0][0] == mock_create_char
                assert mock_to_thread.call_args[0][1] == 12345
