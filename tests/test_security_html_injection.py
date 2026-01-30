import sys
import os
import unittest
from unittest.mock import MagicMock, AsyncMock, patch
import importlib

# Helper to load the root gardarika package
def load_root_gardarika():
    # Remove gardarika from sys.modules if it's the wrong one (from src)
    # We check if 'gardarika.character' is missing, which implies it's the src one
    if 'gardarika' in sys.modules and not hasattr(sys.modules['gardarika'], 'character'):
         # Clean up all gardarika submodules
        to_remove = [k for k in sys.modules if k.startswith('gardarika')]
        for k in to_remove:
            del sys.modules[k]

    # Insert root into sys.path if not there or not first
    root_path = os.path.abspath(".")
    if sys.path[0] != root_path:
        sys.path.insert(0, root_path)

    import gardarika
    import gardarika.character.character
    return gardarika

class TestSecurityHTMLInjection(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Ensure we have the correct gardarika loaded
        self.gardarika = load_root_gardarika()
        # Also need to make sure bot is importable
        if 'bot' not in sys.modules:
            import bot
            self.bot = bot
        else:
            self.bot = sys.modules['bot']

    def test_character_str_escapes_html(self):
        """Test that Character.__str__ escapes HTML tags in the name."""
        from gardarika.character.character import Character

        name = "<b>Hacker</b>"
        # We need valid class and faction names for initialization
        char = Character(name, "воин", "kiev")

        output = str(char)

        # Should contain escaped version
        self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", output)
        # Should NOT contain unescaped version
        self.assertNotIn("<b>Hacker</b>", output)

    async def test_bot_profile_escapes_html(self):
        """Test that the profile handler in bot.py escapes HTML tags in the name."""

        # We use patch on the already imported bot module
        with patch('bot.get_character_by_user_id') as mock_get_char:
            # Mock character data
            mock_get_char.return_value = {
                'name': '<b>Hacker</b>',
                'class_name': 'Воин',
                'faction_name': 'Киев',
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

            # Mock Update and Context
            update = MagicMock()
            update.effective_user.id = 123
            update.message.reply_html = AsyncMock()

            context = MagicMock()

            await self.bot.profile(update, context)

            # Verify reply_html was called
            update.message.reply_html.assert_called_once()

            # Check the message content
            args, _ = update.message.reply_html.call_args
            message = args[0]

            self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", message)
            self.assertNotIn("<b>Hacker</b>", message)

if __name__ == '__main__':
    unittest.main()
