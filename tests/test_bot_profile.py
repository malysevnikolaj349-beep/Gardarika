
import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

# Add root directory to sys.path to import bot.py
sys.path.append(os.getcwd())

# Mock gardarika modules before importing bot
sys.modules["gardarika.database.operations"] = MagicMock()
sys.modules["gardarika.character.character"] = MagicMock()
sys.modules["gardarika.character.attributes"] = MagicMock()

import bot  # noqa: E402


@pytest.mark.asyncio
async def test_profile_handler_new_format():
    # Setup mock
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock message.reply_html as AsyncMock because it's awaited
    update.message.reply_html = AsyncMock()

    # Mock DB return value
    # bot.py uses dictionary access character['name'], so we mock that behavior
    character_data = {
        'name': 'TestHero',
        'class_name': 'Warrior',
        'faction_name': 'Faction A',
        'level': 5,
        'experience': 1000,
        'health': 150,
        'mana': 30,
        'strength': 15,
        'dexterity': 10,
        'wisdom': 8,
        'endurance': 12,
        'charisma': 9
    }

    # We need to patch get_character_by_user_id in bot module
    with patch('bot.get_character_by_user_id', return_value=character_data):
        await bot.profile(update, context)

    # Expected new format
    expected_message = (
        "📜 <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        "👤 <b>Имя:</b> TestHero\n"
        "🛡 <b>Класс:</b> Warrior\n"
        "🚩 <b>Фракция:</b> Faction A\n"
        "📊 <b>Уровень:</b> 5 (Опыт: 1000)\n"
        "❤️ <b>Здоровье:</b> 150\n"
        "💧 <b>Мана:</b> 30\n\n"
        "<b>💎 Атрибуты:</b>\n"
        "  💪 Сила: 15\n"
        "  🦶 Ловкость: 10\n"
        "  🦉 Мудрость: 8\n"
        "  🏇 Выносливость: 12\n"
        "  🎭 Харизма: 9"
    )

    update.message.reply_html.assert_called_once_with(expected_message)
