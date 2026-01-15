import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add the root directory to sys.path to ensure we can import bot and gardarika
sys.path.insert(0, os.path.abspath("."))

from bot import profile

@pytest.mark.asyncio
async def test_profile_handler_output_format():
    """
    Verifies that the profile handler sends a message with the expected content.
    This test mocks the database response and Telegram update objects.
    """
    # Mock update and context
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    # Mock character data dictionary (simulating sqlite3.Row)
    # Note: Keys are lowercase as per bot.py usage
    mock_character = {
        'name': 'Yaroslav',
        'class_name': 'Warrior',
        'faction_name': 'Kyiv',
        'level': 5,
        'experience': 1200,
        'health': 150,
        'mana': 30,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 3,
        'endurance': 8,
        'charisma': 4
    }

    # Patch get_character_by_user_id to return our mock character
    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Assert that reply_html was called once
    update.message.reply_html.assert_called_once()

    # Get the message argument passed to reply_html
    args, _ = update.message.reply_html.call_args
    message = args[0]

    # Check for presence of key information and emojis
    assert "📜 <b>ПРОФИЛЬ ГЕРОЯ</b>" in message
    assert "👤 <b>Имя:</b> Yaroslav" in message
    assert "🛡 <b>Класс:</b> Warrior" in message
    assert "🚩 <b>Фракция:</b> Kyiv" in message
    assert "💪 Сила: 10" in message
