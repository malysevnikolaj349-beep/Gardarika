
import sys
import os
import pytest
import html
from unittest.mock import MagicMock, AsyncMock, patch

# Add root directory to sys.path to allow importing bot
sys.path.insert(0, os.path.abspath("."))

from bot import profile
from gardarika.character.character import Character
# Need to mock get_class and get_faction_info because Character.__init__ calls them
from gardarika.character import classes, character

@pytest.mark.asyncio
async def test_profile_html_injection():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock message
    message = MagicMock()
    update.message = message
    message.reply_html = AsyncMock()

    # Mock character data with malicious name
    malicious_name = "<b>Evil</b>"
    character_data = {
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

    # Patch get_character_by_user_id
    with patch('bot.get_character_by_user_id', return_value=character_data):
        await profile(update, context)

        # Check what was passed to reply_html
        args, _ = message.reply_html.call_args
        reply_text = args[0]

        print(f"\nReply text: {reply_text}")

        # Assert that the name part is escaped.
        # "<b>Evil</b>" -> "&lt;b&gt;Evil&lt;/b&gt;"
        assert "&lt;b&gt;Evil&lt;/b&gt;" in reply_text

def test_character_str_html_injection():
    # Mock dependencies
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        # Setup mocks
        mock_class = MagicMock()
        mock_class.name = "<b>Warrior</b>" # Also malicious class name
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {'name': "<b>Kingdom</b>"} # Malicious faction
        mock_get_faction.return_value = mock_faction

        # Create character with malicious name
        char = Character("<b>Player</b>", "Warrior", "Kingdom")

        output = str(char)
        print(f"\nCharacter output: {output}")

        # Check escaping
        assert "&lt;b&gt;Player&lt;/b&gt;" in output
        assert "&lt;b&gt;Warrior&lt;/b&gt;" in output
        assert "&lt;b&gt;Kingdom&lt;/b&gt;" in output
