import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Add project root to sys.path so we can import bot
sys.path.insert(0, os.path.abspath("."))

# Now we can import bot
import bot

# Mock the database operations in bot module before they are used
@pytest.fixture
def mock_db_ops():
    with patch('bot.add_user_if_not_exists') as mock_add, \
         patch('bot.get_character_by_user_id') as mock_get, \
         patch('bot.create_character') as mock_create:
        yield mock_add, mock_get, mock_create

@pytest.mark.asyncio
async def test_start_handler(mock_db_ops):
    mock_add, _, _ = mock_db_ops

    # Mock Update and Context
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "@testuser"
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # Call the handler
    await bot.start(update, context)

    # Verify DB operation was called
    # In the original code, it's called directly.
    # After optimization, it should still be called (wrapped or not, the mock should capture it if we patch 'bot.add_user_if_not_exists')
    # Wait, if we use asyncio.to_thread(func, args), func is still the object we patched.
    # So the mock should be called.
    mock_add.assert_called_once_with(12345)

    # Verify reply
    update.message.reply_html.assert_called_once()
    args, _ = update.message.reply_html.call_args
    assert "Привет, @testuser!" in args[0]

@pytest.mark.asyncio
async def test_profile_handler_exists(mock_db_ops):
    _, mock_get, _ = mock_db_ops

    # Setup mock character return
    mock_get.return_value = {
        'name': 'Bogatyr',
        'class_name': 'Воин',
        'faction_name': 'Киев',
        'level': 5,
        'experience': 1000,
        'health': 100,
        'mana': 20,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 3,
        'endurance': 8,
        'charisma': 4
    }

    # Mock Update
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # Call handler
    await bot.profile(update, context)

    # Verify DB call
    mock_get.assert_called_once_with(12345)

    # Verify reply
    update.message.reply_html.assert_called_once()
    args, _ = update.message.reply_html.call_args
    assert "Bogatyr" in args[0]
    assert "Сила: 10" in args[0]

@pytest.mark.asyncio
async def test_profile_handler_no_char(mock_db_ops):
    _, mock_get, _ = mock_db_ops

    # Setup mock return None
    mock_get.return_value = None

    # Mock Update
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_text = AsyncMock()

    # Call handler
    await bot.profile(update, context)

    # Verify DB call
    mock_get.assert_called_once_with(12345)

    # Verify reply
    update.message.reply_text.assert_called_once()
    args, _ = update.message.reply_text.call_args
    assert "У вас еще нет персонажа" in args[0]
