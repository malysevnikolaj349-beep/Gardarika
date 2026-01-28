import sys
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Adjust path to import bot.py and gardarika package from root
sys.path.insert(0, os.path.abspath("."))
from bot import profile  # noqa: E402
# We need to import Character but we'll mock its dependencies
from gardarika.character.character import Character  # noqa: E402
from gardarika.character.attributes import Attribute  # noqa: E402


class TestBotProfile(unittest.IsolatedAsyncioTestCase):
    @patch('bot.get_character_by_user_id')
    async def test_profile_handler_format(self, mock_get_char):
        # Mock character data as dict (like DB row)
        mock_get_char.return_value = {
            'name': 'TestHero',
            'class_name': 'Warrior',
            'faction_name': 'Kingdom',
            'level': 5,
            'experience': 1000,
            'health': 120,
            'mana': 60,
            'strength': 10,
            'dexterity': 5,
            'wisdom': 3,
            'endurance': 8,
            'charisma': 4
        }

        update = MagicMock()
        update.effective_user.id = 123
        # Async mock for reply_html
        update.message.reply_html = AsyncMock()

        context = MagicMock()

        await profile(update, context)

        args, _ = update.message.reply_html.call_args
        if not args:
            self.fail("reply_html was not called")
        message = args[0]

        # Check for presence of standard emojis
        self.assertIn("📜", message, "Missing Profile Header emoji")
        self.assertIn("👤", message, "Missing Name emoji")
        self.assertIn("🛡️", message, "Missing Class emoji")
        self.assertIn("🚩", message, "Missing Faction emoji")
        self.assertIn("📊", message, "Missing Level emoji")
        self.assertIn("💎", message, "Missing Experience emoji")
        self.assertIn("❤️", message, "Missing Health emoji")
        self.assertIn("💧", message, "Missing Mana emoji")
        self.assertIn("💪", message, "Missing Strength emoji")
        self.assertIn("🧶", message, "Missing Dexterity emoji")
        self.assertIn("🦉", message, "Missing Wisdom emoji")
        self.assertIn("🐴", message, "Missing Endurance emoji")
        self.assertIn("🎭", message, "Missing Charisma emoji")

    def test_character_str_format(self):
        # We need to mock get_class and get_faction_info
        # because Character __init__ uses them
        with patch('gardarika.character.character.get_class') as mock_class, \
             patch('gardarika.character.character.get_faction_info') as mock_faction:  # noqa: E501

            mock_cls_obj = MagicMock()
            mock_cls_obj.name = "Mage"
            mock_cls_obj.base_stats = {
                Attribute.STRENGTH: 1,
                Attribute.DEXTERITY: 2,
                Attribute.WISDOM: 3,
                Attribute.ENDURANCE: 4,
                Attribute.CHARISMA: 5
            }
            mock_class.return_value = mock_cls_obj

            mock_faction.return_value = {'name': 'Forest'}

            char = Character("Merlin", "Mage", "Forest")
            s = str(char)

            self.assertIn("📜", s, "Missing Header emoji in Character.__str__")
            self.assertIn("👤", s, "Missing Name emoji in Character.__str__")
            self.assertIn("🛡️", s, "Missing Class emoji in Character.__str__")
            self.assertIn("🚩", s, "Missing Faction emoji in Character.__str__")
            self.assertIn("📊", s, "Missing Level emoji in Character.__str__")
            self.assertIn("❤️", s, "Missing Health emoji in Character.__str__")
            self.assertIn("💧", s, "Missing Mana emoji in Character.__str__")
            # Attributes
            self.assertIn("💪", s, "Missing Strength emoji")
            self.assertIn("🧶", s, "Missing Dexterity emoji")
            self.assertIn("🦉", s, "Missing Wisdom emoji")
            self.assertIn("🐴", s, "Missing Endurance emoji")
            self.assertIn("🎭", s, "Missing Charisma emoji")


if __name__ == '__main__':
    unittest.main()
