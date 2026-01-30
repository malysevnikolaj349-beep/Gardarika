# tests/test_bot_profile_ux.py
import sys
import os
import unittest
from unittest.mock import MagicMock, patch, AsyncMock

# Adjust sys.path to include the root directory
sys.path.insert(0, os.path.abspath("."))

# Remove conflicting modules if they exist
keys_to_remove = [k for k in sys.modules if k.startswith('gardarika')]
for k in keys_to_remove:
    del sys.modules[k]

# noqa: E402
from gardarika.character.character import Character  # noqa: E402
from gardarika.character.attributes import Attribute  # noqa: E402
# We need to import bot, but it imports gardarika.database.operations
# which we want to mock.
import bot  # noqa: E402


class TestBotProfileUX(unittest.IsolatedAsyncioTestCase):
    async def test_profile_output_format(self):
        # Mock update and context
        update = MagicMock()
        context = MagicMock()
        update.effective_user.id = 12345
        update.message.reply_html = AsyncMock()

        # Mock character data
        character_data = {
            'name': 'TestHero',
            'class_name': 'Warrior',
            'faction_name': 'Kyiv',
            'level': 5,
            'experience': 1000,
            'health': 150,
            'mana': 60,
            'strength': 10,
            'dexterity': 5,
            'wisdom': 3,
            'endurance': 8,
            'charisma': 4
        }

        with patch(
            'bot.get_character_by_user_id', return_value=character_data
        ):
            await bot.profile(update, context)

        # Check arguments passed to reply_html
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Verify emojis presence
        expected_emojis = [
            '📜', '👤', '🛡️', '🚩', '📊', '💎', '❤️', '💧',
            '💪', '🧶', '🦉', '🐴', '🎭'
        ]

        for emoji in expected_emojis:
            self.assertIn(
                emoji, message, f"Emoji {emoji} not found in profile message"
            )

    def test_character_str_format(self):
        # Mock dependencies for Character init
        with patch('gardarika.character.character.get_class') as mock_class_fn, \
             patch('gardarika.character.character.get_faction_info') as mock_fac_fn:  # noqa: E501

            mock_class = MagicMock()
            mock_class.name = 'Mage'
            mock_class.base_stats = {
                Attribute.STRENGTH: 1,
                Attribute.DEXTERITY: 2,
                Attribute.WISDOM: 10,
                Attribute.ENDURANCE: 3,
                Attribute.CHARISMA: 5
            }
            mock_class_fn.return_value = mock_class

            mock_faction = {'name': 'Novgorod'}
            mock_fac_fn.return_value = mock_faction

            char = Character("Merlin", "Mage", "Novgorod")
            char_str = str(char)

            # Verify emojis presence
            expected_emojis = [
                '📜', '👤', '🛡️', '🚩', '📊', '💎', '❤️', '💧',
                '💪', '🧶', '🦉', '🐴', '🎭'
            ]

            for emoji in expected_emojis:
                self.assertIn(
                    emoji, char_str,
                    f"Emoji {emoji} not found in Character.__str__"
                )
