import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
import pytest

# DEBUG: Print initial sys.path
# print(f"Initial sys.path: {sys.path}")

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# Remove src from sys.path if present
if str(SRC) in sys.path:
    sys.path.remove(str(SRC))

# Ensure ROOT is at the beginning
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
else:
    # Move to front if it wasn't
    sys.path.remove(str(ROOT))
    sys.path.insert(0, str(ROOT))

# Clean sys.modules of any 'gardarika' modules loaded from src
for module_name in list(sys.modules.keys()):
    if module_name == 'gardarika' or module_name.startswith('gardarika.'):
        # Check file path if possible
        module = sys.modules[module_name]
        if hasattr(module, '__file__') and module.__file__:
            if 'src/gardarika' in module.__file__:
                del sys.modules[module_name]

# Now import bot
try:
    import bot
    from gardarika.character.character import Character
except ImportError:
    # If it fails, maybe we need to mock gardarika.database?
    # But here we just want to ensure it loads the correct package.
    raise


@pytest.mark.asyncio
async def test_profile_html_injection():
    # Mock user
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "<a href='tg://user?id=12345'>Test User</a>"  # noqa: E501

    # Mock update
    update = MagicMock()
    update.effective_user = user
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    # Mock context
    context = MagicMock()

    # Mock character data with malicious name
    malicious_name = "<b>HACK</b>"

    # We need to simulate sqlite3.Row access which allows string indexing
    # But simple dict works for ['name'] access
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

    # Patch get_character_by_user_id in bot module
    with patch('bot.get_character_by_user_id', return_value=character_data):
        await bot.profile(update, context)

    # Check what was sent
    update.message.reply_html.assert_called_once()
    args, kwargs = update.message.reply_html.call_args
    message_text = args[0]

    print(f"\nMessage text sent: {message_text}\n")

    # We assert that the vulnerability is FIXED (escaped HTML)
    # The name should be escaped, so <b>HACK</b> becomes &lt;b&gt;HACK&lt;/b&gt;
    expected_escaped_name = "&lt;b&gt;HACK&lt;/b&gt;"

    assert f"<b>Имя:</b> {expected_escaped_name}" in message_text
    assert f"<b>Имя:</b> {malicious_name}" not in message_text


def test_character_str_html_injection():
    """Test that Character.__str__ escapes the name."""
    malicious_name = "<b>HACK</b>"
    # Create a character
    # Use valid class 'воин' and faction 'novgorod'
    char = Character(malicious_name, "воин", "novgorod")

    char_str = str(char)
    print(f"\nCharacter string: {char_str}\n")

    # Expect escaped name
    expected_escaped_name = "&lt;b&gt;HACK&lt;/b&gt;"

    assert f"<b>Имя:</b> {expected_escaped_name}" in char_str
    assert f"<b>Имя:</b> {malicious_name}" not in char_str
