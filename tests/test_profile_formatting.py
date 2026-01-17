
import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root to sys.path so we can import bot and gardarika
sys.path.insert(0, os.path.abspath("."))

from gardarika.character.character import Character
from gardarika.character.attributes import Attribute
from bot import profile

@pytest.mark.asyncio
async def test_bot_profile_formatting():
    # Mock update and context
    update = MagicMock()
    update.effective_user.id = 123
    update.message.reply_html = AsyncMock()

    context = MagicMock()

    # Mock character data returned by database
    # Assuming get_character_by_user_id returns a dict-like object (sqlite3.Row)
    character_data = {
        'name': 'TestHero',
        'class_name': 'Warrior',
        'faction_name': 'Novgorod',
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
    with patch('bot.get_character_by_user_id', return_value=character_data):
        await profile(update, context)

    # Check that reply_html was called
    assert update.message.reply_html.called

    # Get the arguments passed to reply_html
    args, _ = update.message.reply_html.call_args
    message = args[0]

    # Print message for debugging purposes (will show up in failed test output)
    print("\nBot Profile Message:\n", message)

    # Verify NEW format elements
    assert "📜 <b>TestHero</b>" in message
    assert "🛡️ <b>Класс:</b> Warrior" in message
    assert "✨ Атрибуты:" in message
    assert "💎 Сила: 10" in message
    assert "🧶 Ловкость: 5" in message
    assert "🐎 Выносливость: 8" in message


def test_character_str_formatting():
    # Mock dependencies for Character creation
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        mock_class = MagicMock()
        mock_class.name = "Mage"
        # Using Attribute enum keys for base stats
        mock_class.base_stats = {Attribute.STRENGTH: 1, Attribute.WISDOM: 10}
        mock_get_class.return_value = mock_class

        mock_get_faction.return_value = {'name': 'Kiev'}

        char = Character("Merlin", "Mage", "Kiev")

        output = str(char)
        print("\nCharacter Str Output:\n", output)

        # Verify NEW format
        assert "📜 <b>ПРОФИЛЬ ГЕРОЯ</b>" in output
        assert "🛡️ <b>Класс:</b> Mage" in output
        assert "✨ Атрибуты:" in output
        assert "💎 Сила: 1" in output
        assert "🧶 Ловкость: 0" in output
        assert "🐎 Выносливость: 0" in output
