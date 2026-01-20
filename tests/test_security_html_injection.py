import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os
import html

# Ensure root is in path
sys.path.insert(0, os.path.abspath("."))

from bot import profile
from gardarika.character.character import Character

@pytest.mark.asyncio
async def test_profile_html_injection_fix():
    # Mock update and context
    update = MagicMock()
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    user = MagicMock()
    user.id = 123
    update.effective_user = user

    malicious_name = "<b>Hacker</b>"

    mock_character = {
        'name': malicious_name,
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
    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Check what was sent
    args, _ = update.message.reply_html.call_args
    message = args[0]

    # Assert that the malicious name is NOT present in its raw form
    # Note: We look for "<b>Имя:</b> <b>Hacker</b>" which would be the result of injection
    assert f"<b>Имя:</b> {malicious_name}" not in message, "HTML Injection detected!"

    # Assert that the escaped version IS present
    escaped_name = html.escape(malicious_name)
    assert f"<b>Имя:</b> {escaped_name}" in message, "Escaped name not found in message"

def test_character_str_html_injection_fix():
    malicious_name = "<b>Hacker</b>"

    # Mock dependencies
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_faction:

        # Setup mocks
        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = {'name': 'Kingdom'}
        mock_get_faction.return_value = mock_faction

        # Create character
        char = Character(malicious_name, "warrior", "kingdom")

        # Get string representation
        char_str = str(char)

        # Assert that the malicious name is NOT present in its raw form
        assert f"👤 <b>Имя:</b> {malicious_name}" not in char_str, "HTML Injection detected in __str__!"

        # Assert that the escaped version IS present
        escaped_name = html.escape(malicious_name)
        assert f"👤 <b>Имя:</b> {escaped_name}" in char_str, "Escaped name not found in __str__"
