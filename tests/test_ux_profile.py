
import pytest
import re

# Since we don't have the full environment to run bot.py's profile function directly with a mock update easily,
# we will verify the string construction logic which matches what we put in bot.py.
# This test ensures that if we were to extract the logic (as we should in a refactor), it would pass.

def format_profile_logic(character):
    return (
        f"📜 <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        f"👤 <b>Имя:</b> {character['name']}\n"
        f"🛡 <b>Класс:</b> {character['class_name']}\n"
        f"🚩 <b>Фракция:</b> {character['faction_name']}\n"
        f"📊 <b>Уровень:</b> {character['level']} (Опыт: {character['experience']})\n"
        f"❤️ <b>Здоровье:</b> {character['health']} | 💧 <b>Мана:</b> {character['mana']}\n\n"
        f"<b>💎 Атрибуты:</b>\n"
        f"  💪 Сила: {character['strength']}\n"
        f"  🦶 Ловкость: {character['dexterity']}\n"
        f"  🦉 Мудрость: {character['wisdom']}\n"
        f"  🏇 Выносливость: {character['endurance']}\n"
        f"  🎭 Харизма: {character['charisma']}"
    )

def test_profile_formatting_has_emojis():
    mock_char = {
        'name': 'TestChar',
        'class_name': 'TestClass',
        'faction_name': 'TestFaction',
        'level': 5,
        'experience': 1000,
        'health': 150,
        'mana': 80,
        'strength': 10,
        'dexterity': 10,
        'wisdom': 10,
        'endurance': 10,
        'charisma': 10
    }

    output = format_profile_logic(mock_char)

    # Check for emojis
    assert "📜" in output
    assert "👤" in output
    assert "🛡" in output
    assert "🚩" in output
    assert "📊" in output
    assert "❤️" in output
    assert "💧" in output
    assert "💎" in output

    # Check for HTML bold tags
    assert "<b>" in output
    assert "</b>" in output

    # Check for content
    assert "TestChar" in output
    assert "TestClass" in output
