import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root directory to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))
# noqa: E402

from bot import profile  # noqa: E402


@pytest.mark.asyncio
async def test_profile_handler_output():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()

    # Mock effective_user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock reply_html (must be AsyncMock)
    update.message.reply_html = AsyncMock()

    # Mock character data
    mock_character = {
        'name': 'TestHero',
        'class_name': 'Воин',
        'faction_name': 'Киев',
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

    # Mock database call
    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Verify reply_html was called
    update.message.reply_html.assert_called_once()

    # Get the arguments passed to reply_html
    args, _ = update.message.reply_html.call_args
    message = args[0]

    # Assert emojis are present
    assert "📜" in message
    assert "👤" in message
    assert "🛡️" in message
    assert "🚩" in message
    assert "📊" in message
    assert "💎" in message
    assert "❤️" in message
    assert "💧" in message
    assert "💪" in message
    assert "🧶" in message
    assert "🦉" in message
    assert "🐴" in message
    assert "🎭" in message

    # Assert content
    assert "TestHero" in message
    assert "Воин" in message
    assert "Киев" in message
