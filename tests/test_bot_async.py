
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import bot
from telegram import User, Message, Chat, Update

@pytest.fixture
def mock_update_context():
    update = MagicMock(spec=Update)
    context = MagicMock(spec=bot.ContextTypes.DEFAULT_TYPE)

    update.effective_user = MagicMock(spec=User)
    update.effective_user.id = 12345
    update.effective_user.mention_html.return_value = "<a href='tg://user?id=12345'>Test User</a>"

    update.message = AsyncMock(spec=Message)
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    return update, context

@pytest.mark.asyncio
async def test_start_handler(mock_update_context):
    update, context = mock_update_context

    with patch('bot.add_user_if_not_exists') as mock_add_user:
        await bot.start(update, context)

        mock_add_user.assert_called_once_with(12345)
        update.message.reply_html.assert_called_once()

@pytest.mark.asyncio
async def test_profile_handler_existing_character(mock_update_context):
    update, context = mock_update_context

    character_data = {
        'name': 'TestName',
        'class_name': 'Warrior',
        'faction_name': 'TestFaction',
        'level': 1,
        'experience': 0,
        'health': 100,
        'mana': 50,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 5,
        'endurance': 5,
        'charisma': 5
    }

    with patch('bot.get_character_by_user_id', return_value=character_data) as mock_get_char:
        await bot.profile(update, context)

        mock_get_char.assert_called_once_with(12345)
        update.message.reply_html.assert_called_once()
        args, _ = update.message.reply_html.call_args
        assert 'TestName' in args[0]

@pytest.mark.asyncio
async def test_profile_handler_no_character(mock_update_context):
    update, context = mock_update_context

    with patch('bot.get_character_by_user_id', return_value=None) as mock_get_char:
        await bot.profile(update, context)

        mock_get_char.assert_called_once_with(12345)
        update.message.reply_text.assert_called_once()
