
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot import profile
from gardarika.character.character import Character
import html

# Test for XSS in profile command
@pytest.mark.asyncio
async def test_profile_xss_vulnerability():
    # Mock update and context
    update = AsyncMock()
    context = MagicMock()
    update.effective_user.id = 12345

    # Malicious input
    malicious_name = "<b>Evil</b>"
    escaped_name = html.escape(malicious_name)

    # Mock database return value
    # Simulating sqlite3.Row as a dict
    mock_character_data = {
        'name': malicious_name,
        'class_name': 'Warrior',
        'faction_name': 'Kingdom',
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

    with patch('bot.get_character_by_user_id', return_value=mock_character_data):
        await profile(update, context)

        # Check if reply_html was called
        assert update.message.reply_html.called

        # Get the arguments passed to reply_html
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # We expect the message to contain the ESCAPED name.
        assert escaped_name in message, f"Expected escaped name '{escaped_name}' in message, but got unescaped or missing."

        # We expect the RAW malicious HTML to NOT be in the message
        # (This ensures it was escaped and not just passed through)
        assert malicious_name not in message, "Malicious name should be escaped and not present as raw HTML."

# Test for XSS in Character.__str__
def test_character_str_xss():
    malicious_name = "<script>alert('xss')</script>"
    # We need to mock get_class and get_faction_info because Character.__init__ uses them
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {'name': 'Kingdom'}
        mock_get_faction.return_value = mock_faction

        char = Character(malicious_name, "warrior", "kingdom")

        output = str(char)

        # We expect the name to be escaped in the output
        escaped_name = html.escape(malicious_name)
        assert escaped_name in output
        assert malicious_name not in output
