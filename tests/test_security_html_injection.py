import sys
import os
import pytest

# Ensure we are importing the 'gardarika' package from the root, not src/
# This is necessary because src/gardarika also exists and might be prioritized by conftest
sys.path.insert(0, os.path.abspath("."))

try:
    from gardarika.character.character import Character
except ImportError:
    # If the import fails, it might be because of the package structure.
    # We'll try to debug it if it happens.
    raise

def test_character_str_html_injection():
    """
    Test that the Character string representation escapes user-provided HTML content.
    This prevents HTML injection vulnerabilities in Telegram messages.
    """
    # Setup
    unsafe_name = "<b>Hacker</b>"
    # Using existing valid class and faction names (keys in dicts are lowercase)
    char_class = "воин"
    faction = "kiev"

    # Create character
    # Note: This does not interact with DB, so we don't need to mock DB operations
    # unless Character.__init__ does.
    # Checking code: Character.__init__ uses get_class and get_faction_info (static data).
    character = Character(unsafe_name, char_class, faction)

    # Act
    output = str(character)

    # Assert
    # We expect the HTML tags to be escaped in the output
    # HTML escaped version of "<b>Hacker</b>" is "&lt;b&gt;Hacker&lt;/b&gt;"
    expected_escaped_name = "&lt;b&gt;Hacker&lt;/b&gt;"

    # This assertion is expected to FAIL before the fix
    assert expected_escaped_name in output, f"Expected escaped name '{expected_escaped_name}' in output, but got: {output}"

    # Also ensure the original unsafe string is NOT present as-is
    assert unsafe_name not in output, f"Found unsafe HTML '{unsafe_name}' in output!"
