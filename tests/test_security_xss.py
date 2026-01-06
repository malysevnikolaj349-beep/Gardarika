import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os
import html

# Ensure we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gardarika.character.character import Character
from bot import profile

@pytest.fixture
def mock_dependencies():
    with patch('gardarika.character.character.get_class') as mock_class, \
         patch('gardarika.character.character.get_faction_info') as mock_faction:

        mock_class_obj = MagicMock()
        mock_class_obj.name = "Воин"
        mock_class_obj.base_stats = {}
        mock_class.return_value = mock_class_obj

        mock_faction.return_value = {"name": "Киев"}

        yield mock_class, mock_faction

def test_character_str_xss(mock_dependencies):
    """Test that Character.__str__ escapes HTML in the name."""
    name = "<b>Evil</b>"
    char = Character(name, "warrior", "kiev")

    # We expect the name to be escaped in the output
    # Behavior (secure): "<b>Имя:</b> &lt;b&gt;Evil&lt;/b&gt;"

    assert html.escape(name) in str(char)
    assert f"<b>Имя:</b> {html.escape(name)}" in str(char)

@pytest.mark.asyncio
async def test_bot_profile_xss():
    """Test that bot.profile escapes HTML in the character name."""
    update = AsyncMock()
    context = AsyncMock()
    update.effective_user.id = 12345

    character_data = {
        'name': '<b>Evil</b>',
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

    with patch('bot.get_character_by_user_id', return_value=character_data):
        await profile(update, context)

        args, _ = update.message.reply_html.call_args
        message = args[0]

        # We expect the name to be escaped
        assert f"<b>Имя:</b> {html.escape(character_data['name'])}" in message
