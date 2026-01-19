import pytest
from unittest.mock import MagicMock, AsyncMock
from bot import profile
from gardarika.character.character import Character

# Mocking the character data as a dictionary (sqlite3.Row behavior)
MOCK_CHARACTER_DATA = {
    'name': 'TestHero',
    'class_name': 'Warrior',
    'faction_name': 'Kiev',
    'level': 5,
    'experience': 1000,
    'health': 150,
    'mana': 60,
    'strength': 10,
    'dexterity': 5,
    'wisdom': 3,
    'endurance': 8,
    'charisma': 4
}


@pytest.mark.asyncio
async def test_profile_command_output():
    # Setup mocks
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    with pytest.MonkeyPatch.context() as m:
        m.setattr(
            'bot.get_character_by_user_id',
            lambda user_id: MOCK_CHARACTER_DATA
        )

        await profile(update, context)

        # Verify the call
        update.message.reply_html.assert_called_once()
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Check for expected content with new Emoji Tokens
        assert "👤 <b>Имя:</b> TestHero" in message
        assert "🛡️ <b>Класс:</b> Warrior" in message
        assert "🚩 <b>Фракция:</b> Kiev" in message
        assert "📊 <b>Уровень:</b> 5" in message
        assert "❤️ <b>Здоровье:</b> 150" in message
        assert "💧 <b>Мана:</b> 60" in message

        # Attributes Header (Sparkles)
        assert "✨ Атрибуты:" in message

        # Attribute Stats
        assert "💎 Сила: 10" in message
        assert "🧶 Ловкость: 5" in message
        assert "🦉 Мудрость: 3" in message
        assert "🐎 Выносливость: 8" in message
        assert "🎭 Харизма: 4" in message


def test_character_class_str_output():
    char = Character(
        name="TestChar",
        character_class_name="воин",
        faction_name="kiev"
    )

    output = str(char)

    assert "👤 <b>Имя:</b> TestChar" in output
    assert "🛡️ <b>Класс:</b> Воин" in output
    assert "🚩 <b>Фракция:</b> Киевское Княжество" in output
    # Warrior base Strength is 12
    assert "💎 Сила: 12" in output
