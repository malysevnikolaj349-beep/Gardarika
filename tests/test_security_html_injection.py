import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Add root directory to sys.path to allow importing bot.py
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bot import profile  # noqa: E402


@pytest.mark.asyncio
async def test_profile_html_injection():
    # Mock update and context
    update = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    # Mock character data with malicious payload
    malicious_name = "<script>alert('xss')</script><b>Bold</b>"

    mock_character = {
        'name': malicious_name,
        'class_name': 'Warrior',
        'faction_name': 'Faction',
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

    # Patch the database function in bot.py
    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Verify reply_html was called
    if not update.message.reply_html.called:
        pytest.fail("reply_html was not called")

    args, kwargs = update.message.reply_html.call_args
    message = args[0]

    # Check for escaped characters.
    # We expect < to be &lt; and > to be &gt;
    # If the code is vulnerable, these assertions will fail.
    assert "&lt;script&gt;" in message, (
        f"Malicious script tag was not escaped! Message: {message}"
    )
    assert "&lt;b&gt;Bold&lt;/b&gt;" in message, (
        f"Malicious bold tag was not escaped! Message: {message}"
    )
