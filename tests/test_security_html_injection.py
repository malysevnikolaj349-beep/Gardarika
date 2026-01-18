import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Ensure root is in path to import bot
sys.path.insert(0, os.path.abspath("."))

from bot import profile
from gardarika.character.character import Character

@pytest.mark.asyncio
async def test_profile_html_injection_fixed():
    """
    Verifies that the profile command is NO LONGER vulnerable to HTML injection.
    HTML tags in the name should be escaped.
    """

    # Mock update and context
    update = MagicMock()
    context = MagicMock()

    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()

    # Mock character data with malicious name
    malicious_name = "<b>BoldName</b>"

    # Mock database return value
    # simulate sqlite3.Row access by using a dict
    character_data = {
        'name': malicious_name,
        'class_name': 'Warrior',
        'faction_name': 'Novgorod',
        'level': 1,
        'experience': 0,
        'health': 100,
        'mana': 50,
        'strength': 10,
        'dexterity': 10,
        'wisdom': 10,
        'endurance': 10,
        'charisma': 10
    }

    with patch('bot.get_character_by_user_id', return_value=character_data):
        await profile(update, context)

    # Check what was passed to reply_html
    args, _ = update.message.reply_html.call_args
    message_text = args[0]

    print(f"\nMessage text sent: {message_text}")

    # Assert that the name is escaped in the output
    # "<b>Имя:</b> &lt;b&gt;BoldName&lt;/b&gt;"
    assert f"&lt;b&gt;BoldName&lt;/b&gt;" in message_text
    # And specifically NOT the raw tag (except for the label "<b>Имя:</b>" which is hardcoded)
    assert f"<b>Имя:</b> {malicious_name}" not in message_text

@pytest.mark.asyncio
async def test_character_str_html_injection_fixed():
    """
    Verifies that Character.__str__ is NO LONGER vulnerable to HTML injection.
    """
    malicious_name = "<b>BoldName</b>"

    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {"name": "Novgorod"}
        mock_get_faction.return_value = mock_faction

        char = Character(malicious_name, "warrior", "novgorod")
        output = str(char)

        print(f"\nCharacter.__str__ output: {output}")

        # Verify fix: HTML is escaped
        assert f"&lt;b&gt;BoldName&lt;/b&gt;" in output
