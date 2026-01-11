import asyncio
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from bot import start, profile, create_character_start, choose_faction
from telegram import Update, User, Message, CallbackQuery
from telegram.ext import ContextTypes

class TestBotAsync(unittest.IsolatedAsyncioTestCase):
    async def test_start_calls_db_async(self):
        update = MagicMock(spec=Update)
        update.effective_user = MagicMock(spec=User)
        update.effective_user.id = 12345
        update.effective_user.mention_html.return_value = "@testuser"
        update.message = AsyncMock(spec=Message)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

        with patch('bot.add_user_if_not_exists') as mock_db_op:
            await start(update, context)
            mock_db_op.assert_called_once_with(12345)

    async def test_profile_calls_db_async(self):
        update = MagicMock(spec=Update)
        update.effective_user.id = 12345
        update.message = AsyncMock(spec=Message)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

        with patch('bot.get_character_by_user_id') as mock_db_op:
            mock_db_op.return_value = {
                'name': 'Hero', 'class_name': 'Warrior', 'faction_name': 'Kiev',
                'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
                'strength': 10, 'dexterity': 5, 'wisdom': 5, 'endurance': 8, 'charisma': 4
            }
            await profile(update, context)
            mock_db_op.assert_called_once_with(12345)

    async def test_create_character_start_calls_db_async(self):
        update = MagicMock(spec=Update)
        update.effective_user.id = 12345
        update.message = AsyncMock(spec=Message)
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

        with patch('bot.get_character_by_user_id') as mock_db_op:
            mock_db_op.return_value = None
            await create_character_start(update, context)
            mock_db_op.assert_called_once_with(12345)

    async def test_choose_faction_calls_db_async(self):
        update = MagicMock(spec=Update)
        update.effective_user.id = 12345
        update.callback_query = AsyncMock(spec=CallbackQuery)
        update.callback_query.data = 'kiev'
        context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        context.user_data = {'name': 'Hero', 'class': 'воин', 'faction': 'kiev'}

        with patch('bot.create_character') as mock_db_op, \
             patch('bot.Character') as MockCharacter:

            mock_char_instance = MagicMock()
            mock_char_instance.name = 'Hero'
            mock_char_instance.character_class.name = 'Warrior'
            mock_char_instance.faction = {'name': 'Kiev'}
            mock_char_instance.health = 100
            mock_char_instance.mana = 50
            mock_char_instance.attributes = {}
            MockCharacter.return_value = mock_char_instance

            await choose_faction(update, context)
            mock_db_op.assert_called_once()

if __name__ == '__main__':
    unittest.main()
