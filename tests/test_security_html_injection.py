import sys
import os
import pytest
import html
from unittest.mock import MagicMock, patch, AsyncMock

# Add root directory to sys.path to allow importing bot
sys.path.insert(0, os.path.abspath("."))

from bot import profile
from gardarika.character.character import Character

@pytest.mark.asyncio
async def test_profile_html_injection_fixed():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()

    # Mock database response with malicious payload
    malicious_name = "<b>Evil</b>"
    mock_character_data = {
        'name': malicious_name,
        'class_name': 'Warrior',
        'faction_name': 'Horde',
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

        # Verify that reply_html was called
        update.message.reply_html.assert_called_once()

        # Get the argument passed to reply_html
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Verify it contains the ESCAPED version, not the raw tags
        escaped_name = html.escape(malicious_name) # &lt;b&gt;Evil&lt;/b&gt;

        assert escaped_name in message
        assert f"<b>Имя:</b> {escaped_name}" in message
        # Ensure raw unescaped input is NOT present (except where we put it in test verification)
        # Note: '<b>Evil</b>' as a substring is present if we search for it in `&lt;b&gt;Evil&lt;/b&gt;`? No.
        assert malicious_name not in message

def test_character_str_html_injection_fixed():
    # Test Character.__str__ vulnerability fix

    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        # Setup mocks
        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {'name': 'Horde'}
        mock_get_faction.return_value = mock_faction

        malicious_name = "<i>Italic</i>"
        char = Character(malicious_name, "Warrior", "Horde")

        output = str(char)

        # Check for escaped input
        escaped_name = html.escape(malicious_name)
        assert f"👤 <b>Имя:</b> {escaped_name}" in output
        assert malicious_name not in output
