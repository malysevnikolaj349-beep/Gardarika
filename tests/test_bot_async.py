import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root to sys.path to allow importing bot
sys.path.insert(0, os.path.abspath("."))

import bot

@pytest.mark.asyncio
async def test_start_handler_async_db():
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.effective_user.mention_html.return_value = "User"
    update.message.reply_html = AsyncMock()

    # Mock the DB function imported in bot
    with patch('bot.add_user_if_not_exists') as mock_db_call, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        await bot.start(update, context)

        # It should verify that add_user_if_not_exists was passed to asyncio.to_thread
        mock_to_thread.assert_called_with(mock_db_call, 12345)

@pytest.mark.asyncio
async def test_profile_handler_async_db():
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()

    # Mock character data
    mock_char = {
        'name': 'TestChar', 'class_name': 'Warrior', 'faction_name': 'Kiev',
        'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
        'strength': 10, 'dexterity': 10, 'wisdom': 10, 'endurance': 10, 'charisma': 10
    }

    with patch('bot.get_character_by_user_id') as mock_db_call, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        mock_to_thread.return_value = mock_char

        await bot.profile(update, context)

        mock_to_thread.assert_called_with(mock_db_call, 12345)

@pytest.mark.asyncio
async def test_create_character_start_async_db():
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_text = AsyncMock()

    with patch('bot.get_character_by_user_id') as mock_db_call, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        mock_to_thread.return_value = None # No character yet

        await bot.create_character_start(update, context)

        mock_to_thread.assert_called_with(mock_db_call, 12345)

@pytest.mark.asyncio
async def test_choose_faction_async_db():
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    query = MagicMock()
    update.callback_query = query
    query.data = "kiev"
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()

    # Setup context user_data
    context.user_data = {
        'name': 'Hero',
        'class': 'воин', # Matches callback data in bot.py
        'faction': 'kiev'
    }

    # Mock Character class since it's instantiated in handler
    with patch('bot.Character') as MockCharacter, \
         patch('bot.create_character') as mock_create_char, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        # Setup MockCharacter instance
        mock_char_instance = MagicMock()
        mock_char_instance.name = 'Hero'
        mock_char_instance.character_class.name = 'Warrior'
        mock_char_instance.faction = {'name': 'Kiev'}
        mock_char_instance.health = 100
        mock_char_instance.mana = 50
        # attributes should return 0 for keys
        mock_char_instance.attributes.get.return_value = 0

        MockCharacter.return_value = mock_char_instance

        await bot.choose_faction(update, context)

        # Verify create_character is passed to to_thread
        assert mock_to_thread.call_args[0][0] == mock_create_char
