import sys
import os
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
from pathlib import Path

# --- Environment Setup ---
# We need to make sure we import 'bot' from the root directory
# and 'gardarika' from the root directory (not src/gardarika).

ROOT_DIR = Path(__file__).resolve().parent.parent
# We insert at 0 to prioritize root over src (if src is already in path)
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Remove gardarika if it was already loaded from src (e.g. by conftest)
# This is crucial because bot.py imports gardarika.database which is only in root
if 'gardarika' in sys.modules:
    # Check if it's the wrong one (from src)
    if 'src' in str(sys.modules['gardarika'].__file__):
        del sys.modules['gardarika']
        for key in list(sys.modules.keys()):
            if key.startswith('gardarika.'):
                del sys.modules[key]

# Now we can import bot
import bot
from gardarika.character.character import Character

class TestSecurityHtmlInjection(unittest.IsolatedAsyncioTestCase):
    async def test_profile_html_injection(self):
        # Setup
        update = MagicMock()
        context = MagicMock()
        user = MagicMock()
        user.id = 12345
        update.effective_user = user
        update.message.reply_html = AsyncMock()

        # Malicious input
        malicious_name = "<b>Hacker</b>"

        # Mock character data
        character_data = {
            'name': malicious_name,
            'class_name': 'Warrior',
            'faction_name': 'Kiev',
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

        # We patch get_character_by_user_id inside bot module
        with patch('bot.get_character_by_user_id', return_value=character_data):
            await bot.profile(update, context)

        # Check what was passed to reply_html
        args, _ = update.message.reply_html.call_args
        message_text = args[0]

        # The vulnerability is that <b>Hacker</b> is passed directly.
        # We want to assert that it is ESCAPED.
        # Expected: ... <b>Имя:</b> &lt;b&gt;Hacker&lt;/b&gt; ...

        self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", message_text)
        self.assertNotIn(malicious_name, message_text.replace("<b>Имя:</b>", ""))

    async def test_character_str_html_injection(self):
        # We need to test Character.__str__
        # We need to patch get_class and get_faction_info to avoid loading real data/errors

        with patch('gardarika.character.character.get_class') as mock_get_class, \
             patch('gardarika.character.character.get_faction_info') as mock_get_faction:

            # Setup mocks
            mock_class = MagicMock()
            mock_class.name = "Warrior"
            mock_class.base_stats = {}
            mock_get_class.return_value = mock_class

            mock_faction = {'name': 'Kiev'}
            mock_get_faction.return_value = mock_faction

            malicious_name = "<b>Hacker</b>"
            char = Character(malicious_name, "warrior", "kiev")

            output = str(char)

            self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", output)

if __name__ == '__main__':
    unittest.main()
