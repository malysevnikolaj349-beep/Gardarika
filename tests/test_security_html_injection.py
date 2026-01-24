
import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root directory to sys.path to import bot and gardarika
sys.path.insert(0, os.path.abspath("."))

from gardarika.character.character import Character
# We need to import bot, but bot executes code on import (logging setup is fine, but if it runs main it's bad).
# bot.py has if __name__ == "__main__", so it's safe to import.
import bot

class TestSecurityHTMLInjection:

    def test_character_str_escapes_html(self):
        """Test that Character.__str__ escapes HTML in the name."""
        name_with_html = "<b>Hacker</b>"
        # We need to mock classes and faction info since they might rely on external data or files
        # However, checking gardarika/character/character.py, it imports get_class and get_faction_info.
        # If those work without DB, we are fine. The previous reproduction script worked without mocks.
        # Assuming "воин" and "kiev" exist.

        char = Character(name_with_html, "воин", "kiev")
        output = str(char)

        # Verify that the raw HTML tag is NOT present
        assert "<b>Hacker</b>" not in output
        # Verify that the escaped version IS present
        # html.escape converts < to &lt; and > to &gt;
        assert "&lt;b&gt;Hacker&lt;/b&gt;" in output

    @pytest.mark.asyncio
    async def test_bot_profile_escapes_html(self):
        """Test that bot.profile escapes HTML in the character name."""

        # Mock update and context
        update = MagicMock()
        context = MagicMock()

        # Mock user
        user = MagicMock()
        user.id = 12345
        update.effective_user = user

        # Mock reply_html - this is an async method
        update.message.reply_html = AsyncMock()

        # Mock database response
        # The bot expects a dictionary-like object.
        character_data = {
            'name': '<b>Hacker</b>',
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

        # Patch get_character_by_user_id in bot module
        with patch('bot.get_character_by_user_id', return_value=character_data):
            await bot.profile(update, context)

            # Check what was called
            args, _ = update.message.reply_html.call_args
            message = args[0]

            # Verify escaping
            assert "<b>Hacker</b>" not in message
            assert "&lt;b&gt;Hacker&lt;/b&gt;" in message
