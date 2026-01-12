import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from gardarika.character.character import Character
from bot import profile

# Mock database operations
@pytest.fixture
def mock_db_operations():
    with patch('bot.get_character_by_user_id') as mock_get:
        yield mock_get

@pytest.fixture
def mock_character_class():
    with patch('gardarika.character.character.get_class') as mock_class:
        mock_cls = MagicMock()
        mock_cls.name = "Warrior"
        mock_cls.base_stats = {}
        mock_class.return_value = mock_cls
        yield mock_class

@pytest.fixture
def mock_faction_info():
    with patch('gardarika.character.character.get_faction_info') as mock_faction:
        mock_faction.return_value = {'name': "Kiev"}
        yield mock_faction

def test_character_str_xss_vulnerability(mock_character_class, mock_faction_info):
    """
    Test that the Character __str__ method properly escapes HTML in user input.
    """
    malicious_name = "<b>Hacker</b>"
    character = Character(malicious_name, "warrior", "kiev")

    # The name should be escaped, so we expect &lt;b&gt;Hacker&lt;/b&gt;
    assert "<b>Имя:</b> &lt;b&gt;Hacker&lt;/b&gt;" in str(character)

    # Also check a more dangerous injection
    malicious_name_2 = '<a href="http://evil.com">Click me</a>'
    character_2 = Character(malicious_name_2, "warrior", "kiev")
    assert '&lt;a href=&quot;http://evil.com&quot;&gt;Click me&lt;/a&gt;' in str(character_2)

@pytest.mark.asyncio
async def test_bot_profile_xss_vulnerability(mock_db_operations):
    """
    Test that the bot profile handler properly escapes HTML from the database.
    """
    # Setup mock character data with malicious name
    malicious_name = "<b>Hacker</b>"
    mock_character_data = {
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
    mock_db_operations.return_value = mock_character_data

    # Setup mock update and context
    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()

    # Call the profile handler
    await profile(update, context)

    # Verify that reply_html was called with the malicious content
    # The vulnerability is that the user input is treated as trusted HTML
    args, _ = update.message.reply_html.call_args
    message_text = args[0]

    # The string should contain the escaped HTML
    assert f"<b>Имя:</b> &lt;b&gt;Hacker&lt;/b&gt;" in message_text
