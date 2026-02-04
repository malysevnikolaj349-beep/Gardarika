import unittest
import sys
import os
import html
import importlib
from unittest.mock import MagicMock, AsyncMock, patch

class TestSecurityHTMLInjection(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Prepare environment
        self.original_path = sys.path[:]
        self.original_modules = sys.modules.copy()

        root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Insert root at the beginning
        sys.path.insert(0, root_path)

        # Remove conflicting modules to ensure we load from root
        # We need to remove any 'gardarika' modules that might have been loaded from 'src'
        to_remove = [m for m in sys.modules if m.startswith('gardarika') or m == 'bot']
        for m in to_remove:
            del sys.modules[m]

    def tearDown(self):
        # Restore environment
        sys.path = self.original_path
        # Restore sys.modules
        sys.modules.clear()
        sys.modules.update(self.original_modules)

    def test_character_str_escapes_html(self):
        """Test that Character.__str__ escapes HTML in the name."""
        # Import here to use the modified path
        from gardarika.character.character import Character

        name = "<b>Hacker</b>"
        # Using real classes/factions as they are just data in this repo
        char = Character(name, "Воин", "kiev")
        output = str(char)

        escaped_name = html.escape(name) # &lt;b&gt;Hacker&lt;/b&gt;

        self.assertIn(escaped_name, output)
        self.assertNotIn("<b>Hacker</b>", output)

    async def test_bot_profile_escapes_html(self):
        """Test that the bot profile handler escapes HTML in the name."""
        # Import here to use the modified path
        import bot

        # Setup mock character data
        user_name = "<script>alert('xss')</script>"
        mock_data = {
            'name': user_name,
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

        # We need to patch get_character_by_user_id inside bot module
        with patch('bot.get_character_by_user_id', return_value=mock_data):
            # Mock update and context
            update = MagicMock()
            update.effective_user.id = 12345
            update.effective_user.mention_html.return_value = "User"

            # reply_html must be AsyncMock because it's awaited
            update.message.reply_html = AsyncMock()

            context = MagicMock()

            # Call the handler
            await bot.profile(update, context)

            # Verify arguments passed to reply_html
            args, _ = update.message.reply_html.call_args
            message_sent = args[0]

            escaped_name = html.escape(user_name)

            self.assertIn(escaped_name, message_sent)
            self.assertNotIn(user_name, message_sent)

if __name__ == '__main__':
    unittest.main()
