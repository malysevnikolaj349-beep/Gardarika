import sys
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import html

# Add the root directory to sys.path to allow importing from gardarika and bot
# We insert at 0 to take precedence over src/ inserted by conftest.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gardarika.character.character import Character  # noqa: E402
from gardarika.character.attributes import Attribute  # noqa: E402
from gardarika.character.classes import AVAILABLE_CLASSES  # noqa: E402
from gardarika.lore.world import FACTIONS  # noqa: E402

# Import bot module
# Since bot.py is in the root, we can import it after adding root to path
# We need to mock database operations because bot imports them at top level
sys.modules['gardarika.database.operations'] = MagicMock()
import bot  # noqa: E402

class TestHtmlInjection(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Setup valid class and faction for Character creation
        self.class_name = list(AVAILABLE_CLASSES.keys())[0]
        self.faction_name = list(FACTIONS.keys())[0]

    def test_character_str_html_injection(self):
        """Test that Character.__str__ currently does NOT escape HTML (demonstrating vulnerability)
           or DOES escape it (after fix)."""
        malicious_name = "<b>Hacker</b>"
        character = Character(malicious_name, self.class_name, self.faction_name)

        # Check if the name appears as is in the output (vulnerable)
        # or if it is escaped (secure)
        # Note: Ideally this test should fail if the code is vulnerable, but for now I want to confirm behavior.
        profile_str = str(character)

        # If vulnerable, this will be true. If secured, it should be html.escape(malicious_name)
        # e.g. &lt;b&gt;Hacker&lt;/b&gt;

        escaped_name = html.escape(malicious_name)

        # Assert that the output contains the ESCAPED name, not the raw HTML
        self.assertIn(escaped_name, profile_str)
        self.assertNotIn("<b>Hacker</b>", profile_str)
        print("\n[SECURE] Character.__str__ escapes HTML.")

    async def test_bot_profile_html_injection(self):
        """Test that bot.profile handler sends escaped HTML."""
        malicious_name = "<i>Spy</i>"
        escaped_name = html.escape(malicious_name)
        user_id = 12345

        # Mock character data returned from DB
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

        # Mock get_character_by_user_id in bot module
        with patch('bot.get_character_by_user_id', return_value=mock_character_data):
            # Mock Update and Context
            update = MagicMock()
            update.effective_user.id = user_id
            update.message.reply_html = AsyncMock()
            context = MagicMock()

            await bot.profile(update, context)

            # Check what was sent to reply_html
            args, _ = update.message.reply_html.call_args
            message_sent = args[0]

            self.assertIn(f"<b>Имя:</b> {escaped_name}", message_sent)
            self.assertNotIn(f"<b>Имя:</b> {malicious_name}", message_sent)
            print("\n[SECURE] bot.profile escapes HTML.")

if __name__ == '__main__':
    unittest.main()
