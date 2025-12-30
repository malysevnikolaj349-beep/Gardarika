
import sys
import unittest
import html
from unittest.mock import MagicMock, AsyncMock
from pathlib import Path

# Add project root to sys.path to import bot
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# MOCKING DEPENDENCIES BEFORE IMPORTING BOT
# This is necessary because the project has a split package structure (root vs src)
# and pytest uses 'src', while bot.py uses 'root'.
# By mocking these, we bypass the ImportErrors.
mock_db = MagicMock()
mock_ops = MagicMock()
mock_char = MagicMock()
mock_attr = MagicMock()

sys.modules['gardarika.database'] = mock_db
sys.modules['gardarika.database.operations'] = mock_ops
sys.modules['gardarika.character'] = mock_char
sys.modules['gardarika.character.character'] = mock_char
sys.modules['gardarika.character.attributes'] = mock_attr

import bot

class TestSecurityFixes(unittest.IsolatedAsyncioTestCase):
    async def test_html_injection_prevention_in_profile(self):
        """
        Verify that HTML tags in the character name are escaped when displayed in the profile.
        This prevents users from injecting arbitrary HTML (e.g., links, bold text) into the bot's messages.
        """
        # Mock update and context
        update = MagicMock()
        context = MagicMock()

        # Mock user
        update.effective_user.id = 123

        # malicious name
        malicious_name = '<b>Hacker</b>'

        # We need to mock the function on the imported bot module's namespace
        # (or re-mock the sys.modules one if bot imported it directly)

        # bot.py imports: from gardarika.database.operations import get_character_by_user_id
        # So it is bound to bot.get_character_by_user_id

        bot.get_character_by_user_id = MagicMock(return_value={
            'name': malicious_name,
            'class_name': 'Warrior',
            'faction_name': 'Kyiv',
            'level': 1,
            'experience': 0,
            'health': 100,
            'mana': 10,
            'strength': 10,
            'dexterity': 10,
            'wisdom': 10,
            'endurance': 10,
            'charisma': 10
        })

        update.message.reply_html = AsyncMock()

        await bot.profile(update, context)

        # Check what was sent
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # The message should contain the ESCAPED name, not the raw tags
        escaped_name = html.escape(malicious_name) # &lt;b&gt;Hacker&lt;/b&gt;

        # We expect "<b>Имя:</b> &lt;b&gt;Hacker&lt;/b&gt;"
        expected_fragment = f"<b>Имя:</b> {escaped_name}"

        self.assertIn(expected_fragment, message)

if __name__ == '__main__':
    unittest.main()
