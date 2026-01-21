import asyncio
import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Add root directory to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))
# noqa: E402
import bot

@pytest.mark.asyncio
async def test_start_handler_calls_db():
    # Mock update and context
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "User"
    update.effective_user = user
    update.message.reply_html = MagicMock() # This is usually async, need to handle if awaited

    # In python-telegram-bot, reply_html is an async method
    async def async_reply(*args, **kwargs):
        return None
    update.message.reply_html.side_effect = async_reply

    context = MagicMock()

    # Patch the DB function in bot module
    with patch('bot.add_user_if_not_exists') as mock_db:
        await bot.start(update, context)

        # Verify DB called
        mock_db.assert_called_once_with(12345)

@pytest.mark.asyncio
async def test_profile_handler_calls_db():
    update = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    async def async_reply(*args, **kwargs):
        return None
    update.message.reply_html = MagicMock(side_effect=async_reply)
    update.message.reply_text = MagicMock(side_effect=async_reply)

    context = MagicMock()

    # Mock character data
    mock_char = {
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

    with patch('bot.get_character_by_user_id', return_value=mock_char) as mock_db:
        await bot.profile(update, context)
        mock_db.assert_called_once_with(12345)
