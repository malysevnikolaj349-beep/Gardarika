import sys
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Ensure root directory is in path to import bot
sys.path.insert(0, os.path.abspath("."))

from bot import profile
from gardarika.character.character import Character

@pytest.mark.asyncio
async def test_profile_command_output():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()

    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()

    # Mock character data
    character_data = {
        'name': 'TestUser',
        'class_name': 'Warrior',
        'faction_name': 'Kingdom',
        'level': 1,
        'experience': 0,
        'health': 100,
        'mana': 50,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 5,
        'endurance': 10,
        'charisma': 5
    }

    with patch('bot.get_character_by_user_id', return_value=character_data):
        await profile(update, context)

        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Verify new format with emojis
        assert "📜 <b>Профиль героя</b>" in message
        assert "👤 <b>Имя:</b> TestUser" in message
        assert "🛡️ <b>Класс:</b> Warrior" in message
        assert "🚩 <b>Фракция:</b> Kingdom" in message
        assert "📊 <b>Уровень:</b> 1" in message
        assert "❤️ <b>Здоровье:</b> 100" in message
        assert "💧 <b>Мана:</b> 50" in message

        assert "✨ <b>Атрибуты:</b>" in message
        assert "💎 Сила: 10" in message
        assert "🧶 Ловкость: 5" in message
        assert "🦉 Мудрость: 5" in message
        assert "🐎 Выносливость: 10" in message
        assert "🎭 Харизма: 5" in message

def test_character_str_output():
    # Mock dependencies for Character init
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {'name': 'Kingdom'}
        mock_get_faction.return_value = mock_faction

        char = Character("TestChar", "Warrior", "Kingdom")
        output = str(char)

        # Verify new format with emojis
        assert "📜 <b>ПРОФИЛЬ ГЕРОЯ</b>" in output
        assert "👤 <b>Имя:</b> TestChar" in output
        assert "🛡️ <b>Класс:</b> Warrior" in output

        assert "✨ <b>Атрибуты:</b>" in output
        assert "💎 Сила:" in output
        assert "🧶 Ловкость:" in output
        assert "🦉 Мудрость:" in output
        assert "🐎 Выносливость:" in output
        assert "🎭 Харизма:" in output
