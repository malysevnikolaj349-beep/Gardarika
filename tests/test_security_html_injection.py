import sys
import os
import html
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Ensure root directory is in sys.path and strictly at the top
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
else:
    sys.path.remove(root_path)
    sys.path.insert(0, root_path)

# Clean up sys.modules to remove any 'gardarika' loaded from src/
if 'gardarika' in sys.modules:
    module = sys.modules['gardarika']
    # Check if it's likely from src (has path containing /src/ or doesn't have character)
    if hasattr(module, '__file__') and ('src' in module.__file__ or not hasattr(module, 'character')):
        del sys.modules['gardarika']
        for k in list(sys.modules.keys()):
            if k.startswith('gardarika.'):
                del sys.modules[k]

# We need to mock gardarika.database.operations before importing bot
# because bot imports from it.
sys.modules['gardarika.database.operations'] = MagicMock()

import bot

@pytest.mark.asyncio
async def test_profile_html_injection():
    # Mock the update and context
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock message.reply_html
    update.message.reply_html = AsyncMock()

    # Malicious character data
    malicious_name = "<b>Injected</b>"
    # The bot expects a dictionary-like object (sqlite3.Row or dict)
    character_data = {
        'name': malicious_name,
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

    # Mock database call in bot module
    # Note: Since we mocked the module 'gardarika.database.operations' before import,
    # the function 'get_character_by_user_id' in bot.py is already a Mock object.
    # But we can also patch it on 'bot' directly to be sure or just configure the mock.

    with patch('bot.get_character_by_user_id', return_value=character_data):
        await bot.profile(update, context)

    # Check what was sent to reply_html
    args, _ = update.message.reply_html.call_args
    message_text = args[0]

    # Verify fix: The tag should be escaped
    # We expect &lt;b&gt;Injected&lt;/b&gt; in the message
    escaped_name = html.escape(malicious_name)
    assert f"<b>Имя:</b> {escaped_name}" in message_text
    assert malicious_name not in message_text.replace(escaped_name, "") # Ensure raw tag is not present elsewhere
