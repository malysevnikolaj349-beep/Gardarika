import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Ensure root is in path to import bot
sys.path.insert(0, os.path.abspath("."))

from bot import start, profile, create_character_start, choose_faction, CHOOSING_NAME
from gardarika.database.operations import (
    add_user_if_not_exists,
    get_character_by_user_id,
    create_character,
)

@pytest.mark.asyncio
async def test_start_uses_to_thread():
    update = MagicMock()
    context = MagicMock()
    user = update.effective_user
    user.id = 12345

    # Mock message.reply_html to be async
    update.message.reply_html = AsyncMock()

    # We patch asyncio.to_thread to verify it's used
    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        await start(update, context)

        # Verify to_thread was called with the correct DB function
        mock_to_thread.assert_any_call(add_user_if_not_exists, 12345)

@pytest.mark.asyncio
async def test_profile_uses_to_thread():
    update = MagicMock()
    context = MagicMock()
    user = update.effective_user
    user.id = 12345

    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        # Simulate character exists
        mock_to_thread.return_value = {
            'name': 'TestChar', 'class_name': 'Warrior', 'faction_name': 'Kiev',
            'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
            'strength': 10, 'dexterity': 10, 'wisdom': 10, 'endurance': 10, 'charisma': 10
        }

        await profile(update, context)

        mock_to_thread.assert_any_call(get_character_by_user_id, 12345)

@pytest.mark.asyncio
async def test_create_character_start_uses_to_thread():
    update = MagicMock()
    context = MagicMock()
    user = update.effective_user
    user.id = 12345

    update.message.reply_text = AsyncMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        # Simulate no character
        mock_to_thread.return_value = None

        result = await create_character_start(update, context)

        mock_to_thread.assert_any_call(get_character_by_user_id, 12345)
        assert result == CHOOSING_NAME

@pytest.mark.asyncio
async def test_choose_faction_uses_to_thread():
    update = MagicMock()
    context = MagicMock()
    query = update.callback_query
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()

    user_id = 12345
    update.effective_user.id = user_id

    context.user_data = {
        'name': 'Hero',
        'class': 'warrior',
        'faction': 'kiev'
    }

    # Patch Character class so we don't depend on validation logic
    with patch('bot.Character') as MockCharacter:
        mock_instance = MockCharacter.return_value
        mock_instance.name = 'Hero'
        mock_instance.character_class.name = 'Warrior'
        mock_instance.faction = {'name': 'Kiev'}
        mock_instance.health = 100
        mock_instance.mana = 50
        mock_instance.attributes = {}

        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            await choose_faction(update, context)

            # Verify create_character was passed to to_thread
            # We check that create_character is the first argument
            # Note: assert_any_call checks if it was called *at some point*.
            # Since create_character is the *first argument* to to_thread, we check arguments.

            # We need to find the call where arg[0] is create_character
            found = False
            for call in mock_to_thread.call_args_list:
                args, _ = call
                if args[0] == create_character:
                    found = True
                    assert args[1] == user_id
                    break

            assert found, "create_character was not called via asyncio.to_thread"
