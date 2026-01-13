import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Ensure root is in path
sys.path.append(os.getcwd())

from gardarika.character.character import Character
from gardarika.character.attributes import Attribute

# Standardized Emojis as per Design Tokens
EMOJIS = {
    "name": "👤",
    "class": "🛡️",  # Note: 🛡 vs 🛡️ might be tricky, checking strict containment
    "faction": "🚩",
    "level": "📊",
    "health": "❤️",
    "mana": "💧",
    "strength": "💎",
    "dexterity": "🦵",
    "wisdom": "🦉",
    "endurance": "🐎",
    "charisma": "🎭",
    "header": "📜"
}

def test_character_str_formatting():
    # Mock dependencies for Character init
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        # Setup mocks
        mock_class = MagicMock()
        mock_class.name = "Воин"
        # Character init copies base_stats. Attribute keys are Enum members.
        mock_class.base_stats = {Attribute.STRENGTH: 10}
        mock_get_class.return_value = mock_class

        mock_faction = {"name": "Новгород"}
        mock_get_faction.return_value = mock_faction

        char = Character("TestHero", "Warrior", "Novgorod")

        output = str(char)

        # Verify emojis
        for key, emoji in EMOJIS.items():
            assert emoji in output, f"Missing emoji for {key}: {emoji}"

        # Verify formatting
        assert "<b>Имя:</b> TestHero" in output

    # Test escaping in __str__
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:
        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {Attribute.STRENGTH: 10}
        mock_get_class.return_value = mock_class
        mock_faction = {"name": "Novgorod"}
        mock_get_faction.return_value = mock_faction

        char_evil = Character('<script>', "Warrior", "Novgorod")
        assert "&lt;script&gt;" in str(char_evil)
        assert "<script>" not in str(char_evil)

@pytest.mark.asyncio
async def test_bot_profile_formatting():
    from bot import profile

    # Mock update and context
    update = MagicMock()
    update.effective_user.id = 123
    # reply_html must be an async mock if we were awaiting it,
    # but the handler awaits it, so the mock object itself doesn't need to be async,
    # but the return value of the call needs to be awaitable if the handler awaits the result?
    # Actually, `await update.message.reply_html(...)` means `reply_html` returns a coroutine.
    update.message.reply_html = AsyncMock()

    context = MagicMock()

    # Mock DB return
    mock_char_data = {
        'name': '<script>alert("xss")</script>', # Test escaping
        'class_name': 'Воин',
        'faction_name': 'Новгород',
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

    with patch('bot.get_character_by_user_id', return_value=mock_char_data):
        await profile(update, context)

        # Check arguments passed to reply_html
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Verify emojis
        for key, emoji in EMOJIS.items():
            assert emoji in message, f"Missing emoji for {key}: {emoji} in message: {message}"

        # Verify escaping
        assert "&lt;script&gt;" in message
        assert "<script>" not in message
