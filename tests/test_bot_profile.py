import sys
import os
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Add root to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))

from bot import profile

@pytest.mark.asyncio
async def test_profile_command_output():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # Mock character data
    mock_character = {
        'name': 'TestHero',
        'class_name': 'Воин',
        'faction_name': 'Киев',
        'level': 5,
        'experience': 1000,
        'health': 150,
        'mana': 60,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 3,
        'endurance': 8,
        'charisma': 2
    }

    # Patch get_character_by_user_id
    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Verify the output contains emojis
    args, _ = update.message.reply_html.call_args
    message = args[0]

    # Check for all standardized emojis
    assert "👤" in message
    assert "🛡️" in message
    assert "🚩" in message
    assert "📊" in message
    assert "❤️" in message
    assert "💧" in message
    assert "💎" in message
    assert "💪" in message
    assert "🧶" in message # Dexterity
    assert "🦉" in message
    assert "🐴" in message # Endurance
    assert "🎭" in message

    # Check for values
    assert "TestHero" in message
    assert "Воин" in message
    assert "Киев" in message
