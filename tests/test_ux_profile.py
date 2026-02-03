import sys
import os
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

# Ensure root is in path and takes precedence for this test
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# We need to make sure we import the root 'gardarika' package
if 'gardarika' in sys.modules:
    import gardarika
    if not hasattr(gardarika, 'character'):
        del sys.modules['gardarika']
        keys = [k for k in sys.modules.keys() if k.startswith('gardarika.')]
        for k in keys:
            del sys.modules[k]

try:
    from gardarika.character.character import Character
    from gardarika.character.attributes import Attribute
    import bot
except ImportError:
    sys.path.insert(0, ROOT_DIR)
    from gardarika.character.character import Character
    from gardarika.character.attributes import Attribute
    import bot


class TestUXProfile(unittest.IsolatedAsyncioTestCase):
    def test_character_str_emojis(self):
        """Verify that Character.__str__ uses the correct new emojis."""
        with patch(
            'gardarika.character.character.get_class'
        ) as mock_class_fn, patch(
            'gardarika.character.character.get_faction_info'
        ) as mock_faction_fn:

            # Setup mock class
            mock_class = MagicMock()
            mock_class.name = "Воин"
            mock_class.base_stats = {
                Attribute.STRENGTH: 10,
                Attribute.DEXTERITY: 5,
                Attribute.WISDOM: 2,
                Attribute.ENDURANCE: 8,
                Attribute.CHARISMA: 3
            }
            mock_class_fn.return_value = mock_class

            # Setup mock faction
            mock_faction_fn.return_value = {'name': "Киев"}

            char = Character("TestName", "warrior", "kiev")

            output = str(char)

            # Check for new emojis
            self.assertIn("🧶", output, "Dexterity should have 🧶")
            self.assertIn("🐴", output, "Endurance should have 🐴")

    def test_character_str_escaping(self):
        """Verify that Character.__str__ escapes the name."""
        with patch(
            'gardarika.character.character.get_class'
        ) as mock_class_fn, patch(
            'gardarika.character.character.get_faction_info'
        ) as mock_faction_fn:

            mock_class = MagicMock()
            mock_class.name = "Воин"
            mock_class.base_stats = {}
            mock_class_fn.return_value = mock_class
            mock_faction_fn.return_value = {'name': "Киев"}

            char = Character("<b>Bold</b>", "warrior", "kiev")
            output = str(char)

            self.assertIn("&lt;b&gt;Bold&lt;/b&gt;", output)

    async def test_bot_profile_handler(self):
        """Verify that bot.profile sends the correct HTML message."""
        # Mock update and context
        update = MagicMock()
        update.effective_user.id = 123
        update.message.reply_html = AsyncMock()

        context = MagicMock()

        # Mock get_character_by_user_id
        with patch('bot.get_character_by_user_id') as mock_get_char:
            mock_get_char.return_value = {
                'name': '<script>alert(1)</script>',  # Test escaping
                'class_name': 'Воин',
                'faction_name': 'Киев',
                'level': 5,
                'experience': 1000,
                'health': 150,
                'mana': 60,
                'strength': 12,
                'dexterity': 7,
                'wisdom': 4,
                'endurance': 10,
                'charisma': 5
            }

            await bot.profile(update, context)

            # Verify call
            update.message.reply_html.assert_called_once()
            args, _ = update.message.reply_html.call_args
            message = args[0]

            # Check for escaped name
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", message)

            # Check for Standardized Emojis
            self.assertIn("📜 <b>ПРОФИЛЬ ГЕРОЯ</b>", message)
            self.assertIn("👤 <b>Имя:</b>", message)
            self.assertIn("🛡️ <b>Класс:</b>", message)
            self.assertIn("🧶 Ловкость:", message)
            self.assertIn("🐴 Выносливость:", message)
            self.assertIn("💎 1000", message)


if __name__ == '__main__':
    unittest.main()
