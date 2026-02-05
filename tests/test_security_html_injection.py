import unittest
import sys
import os
from unittest.mock import MagicMock, patch, AsyncMock

# Add root directory to sys.path to import gardarika
sys.path.append(os.getcwd())

from gardarika.character.character import Character  # noqa: E402
import bot  # noqa: E402


class TestSecurityHTMLInjection(unittest.IsolatedAsyncioTestCase):
    def test_character_str_html_injection(self):
        """
        Test that Character.__str__ sanitizes the character name
        to prevent HTML injection.
        """
        # Malicious name containing HTML tags
        malicious_name = "<b>Malicious</b>"

        # Create a character with the malicious name
        # Using 'воин' and 'kiev' as valid class and faction
        character = Character(malicious_name, "воин", "kiev")

        # Get the string representation
        profile_str = str(character)

        # Check if the tags are escaped
        # We expect &lt;b&gt;Malicious&lt;/b&gt; instead of <b>Malicious</b>
        if "<b>Malicious</b>" in profile_str:
            self.fail(
                "Vulnerability found! "
                f"Character name not escaped in __str__:\n{profile_str}"
            )

        self.assertIn("&lt;b&gt;Malicious&lt;/b&gt;", profile_str)

    @patch('bot.get_character_by_user_id')
    async def test_bot_profile_html_injection(self, mock_get_character):
        """
        Test that bot.profile handler sanitizes the character name.
        """
        # Setup mock character data with malicious name
        malicious_name = "<b>Malicious</b>"
        mock_character = {
            'name': malicious_name,
            'class_name': 'Воин',
            'faction_name': 'Киевское Княжество',
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
        mock_get_character.return_value = mock_character

        # Mock update and context
        update = MagicMock()
        update.effective_user.id = 12345
        update.effective_user.mention_html.return_value = "User"

        # The reply_html method is awaited, so it should be an AsyncMock
        update.message.reply_html = AsyncMock()

        context = MagicMock()

        # Call the profile handler
        await bot.profile(update, context)

        # Check arguments passed to reply_html
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Check if the tags are escaped
        if "<b>Malicious</b>" in message:
            self.fail(
                "Vulnerability found! "
                f"Character name not escaped in bot.profile:\n{message}"
            )

        self.assertIn("&lt;b&gt;Malicious&lt;/b&gt;", message)


if __name__ == "__main__":
    unittest.main()
