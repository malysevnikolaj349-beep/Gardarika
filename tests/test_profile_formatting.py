import sys
from pathlib import Path

# Ensure root is in path to import bot
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bot import format_profile_message


def test_format_profile_message_structure():
    """
    Test that the profile message formatting matches the expected visual style.
    This test serves as a specification for the implementation.
    """
    # Mock data structure resembling what get_character_by_user_id returns
    character_data = {
        'name': 'Yaroslav',
        'class_name': 'Воин',
        'faction_name': 'Киевское Княжество',
        'level': 1,
        'experience': 0,
        'health': 110,
        'mana': 60,
        'strength': 12,
        'dexterity': 8,
        'wisdom': 5,
        'endurance': 10,
        'charisma': 6
    }

    # Expected format with emojis and HTML tags
    expected_output = (
        "📜 <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        "👤 <b>Имя:</b> Yaroslav\n"
        "🛡 <b>Класс:</b> Воин\n"
        "🚩 <b>Фракция:</b> Киевское Княжество\n"
        "📊 <b>Уровень:</b> 1 (Опыт: 0)\n"
        "❤️ <b>Здоровье:</b> 110\n"
        "💧 <b>Мана:</b> 60\n\n"
        "<b>💎 Атрибуты:</b>\n"
        "  💪 Сила: 12\n"
        "  🦶 Ловкость: 8\n"
        "  🦉 Мудрость: 5\n"
        "  🏇 Выносливость: 10\n"
        "  🎭 Харизма: 6"
    )

    assert format_profile_message(character_data) == expected_output
