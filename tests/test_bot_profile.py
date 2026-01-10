import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot import profile

@pytest.mark.asyncio
async def test_profile_command_output_with_emojis():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()

    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()

    # Mock database response
    # Simulating sqlite3.Row behavior with a dict
    mock_character = {
        'name': 'TestHero',
        'class_name': 'Warrior',
        'faction_name': 'TestFaction',
        'level': 5,
        'experience': 1000,
        'health': 150,
        'mana': 30,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 2,
        'endurance': 8,
        'charisma': 3
    }

    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Check that reply_html was called
    assert update.message.reply_html.called

    # Get the message content
    args, _ = update.message.reply_html.call_args
    message = args[0]

    # Verify emojis and structure are present (Palette's improvement)
    assert "📜 <b>ПРОФИЛЬ ГЕРОЯ</b>" in message
    assert "👤 <b>Имя:</b> TestHero" in message
    assert "🛡 <b>Класс:</b> Warrior" in message
    assert "🚩 <b>Фракция:</b> TestFaction" in message
    assert "📊 <b>Уровень:</b> 5 (XP: 1000)" in message
    assert "❤️ <b>Здоровье:</b> 150" in message
    assert "💧 <b>Мана:</b> 30" in message
    assert "<b>💎 Атрибуты:</b>" in message
    assert "💪 Сила: 10" in message
    assert "🦶 Ловкость: 5" in message
    assert "🦉 Мудрость: 2" in message
    assert "🏇 Выносливость: 8" in message
    assert "🎭 Харизма: 3" in message
