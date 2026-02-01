
import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from telegram import Update, User, Message
from telegram.ext import ContextTypes

# Ensure root directory is in sys.path to import bot and gardarika
# This is needed because the test runs from tests/ or root, and we need to verify imports work.
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
src_dir = os.path.join(root_dir, 'src')

# Clean up sys.path: remove src, add root at beginning
if src_dir in sys.path:
    sys.path.remove(src_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Force re-import of gardarika from root
# Remove gardarika and all submodules from sys.modules
to_remove = [
    m for m in list(sys.modules.keys())
    if m == 'gardarika' or m.startswith('gardarika.')
]
for m in to_remove:
    del sys.modules[m]

import bot  # noqa: E402
from gardarika.character.character import Character  # noqa: E402


@pytest.mark.asyncio
async def test_profile_html_injection():
    """
    Test that the profile handler properly escapes user input
    (name, class, faction) to prevent HTML injection.
    """
    # Mock user and update
    user = MagicMock(spec=User)
    user.id = 123456
    user.mention_html.return_value = "User"

    message = AsyncMock(spec=Message)
    update = MagicMock(spec=Update)
    update.effective_user = user
    update.message = message

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    # Mock character data with malicious HTML
    malicious_name = "<b>Hacker</b>"
    malicious_class = "Warrior<script>"
    malicious_faction = "Rebels</i>"

    character_data = {
        'name': malicious_name,
        'class_name': malicious_class,
        'faction_name': malicious_faction,
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

    # Check what was passed to reply_html
    args, _ = message.reply_html.call_args
    sent_text = args[0]

    # We expect the HTML tags in the name to be escaped.
    # &lt;b&gt;Hacker&lt;/b&gt; instead of <b>Hacker</b>

    # If vulnerability exists:
    # <b>Имя:</b> <b>Hacker</b>

    # If fixed:
    # <b>Имя:</b> &lt;b&gt;Hacker&lt;/b&gt;

    assert "&lt;b&gt;Hacker&lt;/b&gt;" in sent_text, (
        f"Name was not escaped! Got: {sent_text}"
    )
    assert "Warrior&lt;script&gt;" in sent_text, (
        f"Class was not escaped! Got: {sent_text}"
    )
    assert "Rebels&lt;/i&gt;" in sent_text, (
        f"Faction was not escaped! Got: {sent_text}"
    )


def test_character_str_html_injection():
    """
    Test that Character.__str__ properly escapes user input.
    """
    # We need to mock get_class and get_faction_info because
    # Character constructor calls them
    with patch('gardarika.character.character.get_class') as mock_get_class, \
         patch('gardarika.character.character.get_faction_info') as mock_get_f:

        # Mock class data
        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        # Mock faction data
        mock_get_f.return_value = {'name': "Faction"}

        # Create character with malicious name
        char = Character("<b>Hacker</b>", "Warrior", "Faction")

        output = str(char)

        # We expect escaped HTML in the output string
        assert "&lt;b&gt;Hacker&lt;/b&gt;" in output, (
            f"Character name not escaped in __str__! Got: {output}"
        )
