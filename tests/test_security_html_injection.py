import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root directory to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))

# Mock the database operations BEFORE importing bot
sys.modules["gardarika.database.operations"] = MagicMock()

from gardarika.character.character import Character  # noqa: E402
import bot  # noqa: E402


def test_character_str_html_injection():
    """Test that Character.__str__ escapes HTML in the name."""
    # We need to mock get_class and get_faction_info
    # because Character.__init__ uses them
    with patch("gardarika.character.character.get_class") as mock_get_class, \
         patch(
             "gardarika.character.character.get_faction_info"
         ) as mock_get_faction:

        # Setup mocks
        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {"name": "Faction"}
        mock_get_faction.return_value = mock_faction

        # Create character with malicious name
        malicious_name = "<b>Hacker</b>"
        char = Character(malicious_name, "warrior", "faction")

        # Check if the name is escaped in the output
        output = str(char)

        # To fail if it IS vulnerable (for reproduction),
        # we assert that it IS escaped
        # If it's vulnerable, this assertion will fail.
        assert "&lt;b&gt;Hacker&lt;/b&gt;" in output, \
            "Character name not escaped in __str__"


@pytest.mark.asyncio
async def test_bot_profile_html_injection():
    """Test that bot.profile escapes HTML in the name."""
    # Mock update and context
    update = MagicMock()
    update.effective_user.id = 123
    # Use AsyncMock for awaited method
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    # Mock character data
    character_data = {
        'name': '<b>Hacker</b>',
        'class_name': 'Warrior',
        'faction_name': 'Faction',
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

    # We need to patch bot.get_character_by_user_id.
    # Since we mocked the module gardarika.database.operations before import,
    # bot.get_character_by_user_id is already a mock from that module.
    # But we want to set its return value.

    # Actually, bot imports the function directly:
    # from gardarika.database.operations import get_character_by_user_id
    # So bot.get_character_by_user_id is the object.

    with patch("bot.get_character_by_user_id", return_value=character_data):
        await bot.profile(update, context)

        # Check what was passed to reply_html
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # We expect &lt;b&gt;Hacker&lt;/b&gt;
        assert "&lt;b&gt;Hacker&lt;/b&gt;" in message, \
            "Character name not escaped in profile message"
