import sys
import os
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

# Add the root directory to sys.path to allow importing bot.py
sys.path.insert(0, os.path.abspath("."))

# We need to ensure we can import bot.py without executing main()
# bot.py has `if __name__ == "__main__": main()` so it is safe to import.

import bot  # noqa: E402


class TestBotProfile(unittest.IsolatedAsyncioTestCase):
    async def test_profile_command_ux(self):
        # Mock the update and context
        update = MagicMock()
        context = MagicMock()

        # Make reply_html async
        update.message.reply_html = AsyncMock()

        # Mock effective_user.id
        update.effective_user.id = 12345

        # Mock the character data
        character_data = {
            'name': 'TestUser',
            'class_name': 'Воин',
            'faction_name': 'Киев',
            'level': 1,
            'experience': 0,
            'health': 100,
            'mana': 50,
            'strength': 10,
            'dexterity': 5,
            'wisdom': 2,
            'endurance': 8,
            'charisma': 3
        }

        # Patch get_character_by_user_id where it is used in bot.py
        with patch(
            'bot.get_character_by_user_id', return_value=character_data
        ):
            # Call the profile function
            await bot.profile(update, context)

            # Assert that reply_html was called
            update.message.reply_html.assert_called_once()

            # Get the message content
            args, _ = update.message.reply_html.call_args
            message = args[0]

            # Verify the UX improvements (emojis) are present
            # Header
            self.assertIn("📜", message, "Profile header emoji missing")

            # Core stats
            self.assertIn("🛡", message, "Class emoji missing")
            self.assertIn("🚩", message, "Faction emoji missing")
            self.assertIn("📊", message, "Level emoji missing")
            self.assertIn("❤️", message, "Health emoji missing")
            self.assertIn("💧", message, "Mana emoji missing")

            # Attributes
            self.assertIn("💎", message, "Attributes header emoji missing")
            self.assertIn("💪", message, "Strength emoji missing")
            self.assertIn("🧶", message, "Dexterity emoji missing")
            self.assertIn("🦉", message, "Wisdom emoji missing")
            self.assertIn("🐴", message, "Endurance emoji missing")
            self.assertIn("🎭", message, "Charisma emoji missing")


if __name__ == "__main__":
    unittest.main()
