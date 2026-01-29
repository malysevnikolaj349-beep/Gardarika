import sys
import os
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import html

# Do not import bot here


@pytest.mark.asyncio
async def test_profile_html_injection_prevention():
    # AGGRESSIVE ENVIRONMENT RESET for bot.py context

    # 1. Clean sys.path
    # Remove any path ending in 'src'
    sys.path = [
        p for p in sys.path
        if not p.endswith('src') and not p.endswith('src/')
    ]

    # 2. Add root to sys.path if not there
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    # 3. Clear sys.modules of ANY gardarika references to force reload from root
    keys_to_remove = [k for k in sys.modules if k.startswith('gardarika')]
    for k in keys_to_remove:
        del sys.modules[k]

    # Now import bot. It should find root/gardarika
    import bot

    # Setup
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock reply_html (it's async)
    update.message.reply_html = AsyncMock()

    # Malicious name
    malicious_name = "<b>Hacker</b>"

    # Mock database response
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

    # We patch bot.get_character_by_user_id
    with patch('bot.get_character_by_user_id', return_value=character_data):
        await bot.profile(update, context)

    # Verify
    args, _ = update.message.reply_html.call_args
    message_text = args[0]

    # We expect the name to be escaped
    escaped_name = html.escape(malicious_name)

    assert escaped_name in message_text, (
        f"Expected escaped name '{escaped_name}' in message, "
        f"but got: {message_text}"
    )
