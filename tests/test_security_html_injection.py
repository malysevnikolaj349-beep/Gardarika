
import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root directory to sys.path to import bot
sys.path.insert(0, os.path.abspath("."))
# noqa: E402
import bot

@pytest.mark.asyncio
async def test_profile_html_injection():
    # Setup
    user_id = 12345
    malicious_name = "<b>Hacker</b>"

    # Mock update and context
    update = MagicMock()
    update.effective_user.id = user_id
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    # Mock database response
    # The bot expects a dict-like object (or sqlite3.Row)
    character_data = {
        'name': malicious_name,
        'class_name': 'Warrior',
        'faction_name': 'Kyiv',
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

    with patch('bot.get_character_by_user_id', return_value=character_data):
        await bot.profile(update, context)

    # Verification
    args, _ = update.message.reply_html.call_args
    message_text = args[0]

    # The name should be escaped.
    # "<b>Hacker</b>" -> "&lt;b&gt;Hacker&lt;/b&gt;"
    expected_escaped_name = "&lt;b&gt;Hacker&lt;/b&gt;"

    # Assert that the ESCAPED name is in the message
    assert f"<b>Имя:</b> {expected_escaped_name}" in message_text

    # Assert that the RAW malicious name is NOT in the message (except where we expect the escaped version)
    # Since checking for "<b>Hacker</b>" would fail if it's present, but checking for "<b>Имя:</b> <b>Hacker</b>" is more specific.
    assert f"<b>Имя:</b> {malicious_name}" not in message_text
