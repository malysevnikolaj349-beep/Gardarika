import sys
import os
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

# Insert root into path to find bot.py
# We use abspath to ensure it works regardless of where pytest is run from,
# assuming we are running from root.
sys.path.insert(0, os.path.abspath("."))

# Now import bot (which imports gardarika)
# We need to ignore E402 (module level import not at top of file)
import bot # noqa: E402
from bot import start, profile, create_character_start, choose_faction # noqa: E402

@pytest.mark.asyncio
async def test_start_handler():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "<a href='...'>User</a>"
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # Patch the function in bot module
    with patch('bot.add_user_if_not_exists') as mock_db:
        await start(update, context)
        mock_db.assert_called_once_with(12345)
        update.message.reply_html.assert_called_once()

@pytest.mark.asyncio
async def test_profile_handler():
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    # Case 1: Character exists
    # Dictionary mocking Row
    char_data = {
        'name': 'TestChar',
        'class_name': 'Воин',
        'faction_name': 'Киев',
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

    with patch('bot.get_character_by_user_id', return_value=char_data) as mock_db:
        await profile(update, context)
        mock_db.assert_called_once_with(12345)
        update.message.reply_html.assert_called_once()
        args, _ = update.message.reply_html.call_args
        assert 'TestChar' in args[0]

@pytest.mark.asyncio
async def test_create_character_start():
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_text = AsyncMock()

    with patch('bot.get_character_by_user_id', return_value=None) as mock_get:
        res = await create_character_start(update, context)
        mock_get.assert_called_once_with(12345)
        assert res == bot.CHOOSING_NAME

@pytest.mark.asyncio
async def test_choose_faction_creates_character():
    update = MagicMock()
    context = MagicMock()
    query = MagicMock()
    update.callback_query = query
    update.effective_user.id = 12345
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    query.data = 'kiev'

    # Setup context with previous steps
    context.user_data = {
        'name': 'NewHero',
        'class': 'воин',
        'faction': 'kiev' # This will be overwritten by query.data in handler but logic sets it
    }

    # patch create_character
    with patch('bot.create_character') as mock_create:
        res = await choose_faction(update, context)

        mock_create.assert_called_once()
        call_args = mock_create.call_args
        # create_character(user_id, name, class_name, faction_name, stats)
        assert call_args[0][0] == 12345
        assert call_args[0][1] == 'NewHero'
        # The character creation logic in bot.py instantiates Character to get class name
        # We assume real Character logic works here (it's pure logic)

        query.edit_message_text.assert_called()
        assert "Персонаж создан" in query.edit_message_text.call_args[1]['text']
