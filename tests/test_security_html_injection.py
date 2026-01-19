import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import html

# Insert root directory to path
sys.path.insert(0, os.path.abspath("."))

from gardarika.character.character import Character
# Import bot after setting path
import bot

def test_character_str_html_injection():
    """
    Test that Character.__str__ escapes HTML in user-provided fields (name).
    """
    malicious_name = "<b>Evil</b>"
    char = Character(malicious_name, "воин", "kiev")

    output = str(char)

    assert "<b>Evil</b>" not in output, "XSS Vulnerability: Name is not escaped in __str__"
    assert "&lt;b&gt;Evil&lt;/b&gt;" in output, "Name should be HTML escaped"

@pytest.mark.asyncio
async def test_bot_profile_html_injection():
    """
    Test that the bot profile handler escapes HTML in user input.
    """
    # Mock update and context
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # Malicious character data
    character_data = {
        'name': '<script>alert(1)</script>',
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

    # Patch get_character_by_user_id
    with patch('bot.get_character_by_user_id', return_value=character_data):
        await bot.profile(update, context)

    # Verify reply_html called with escaped name
    assert update.message.reply_html.called
    args, _ = update.message.reply_html.call_args
    message = args[0]

    assert "<script>" not in message, "XSS Vulnerability: Name is not escaped in bot profile message"
    assert "&lt;script&gt;" in message, "Name should be HTML escaped in bot profile"
