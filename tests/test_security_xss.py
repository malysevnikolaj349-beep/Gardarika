
import pytest
import html
from gardarika.character.character import Character

def test_character_str_escapes_html_in_name():
    """
    Test that Character.__str__ correctly escapes HTML characters in the name,
    preventing HTML injection vulnerabilities.
    """
    # Create a character with a malicious name containing HTML tags
    malicious_name = "<b>Hacker</b>"

    try:
        char = Character(malicious_name, "воин", "kiev")
    except ValueError as e:
        pytest.fail(f"Could not create character: {e}")

    profile_html = str(char)

    # We expect the name to be escaped.
    # html.escape("<b>Hacker</b>") -> "&lt;b&gt;Hacker&lt;/b&gt;"
    expected_safe_name = html.escape(malicious_name)

    # Verify that the unescaped malicious string is NOT present
    assert malicious_name not in profile_html, "Unescaped HTML found in profile!"

    # Verify that the escaped safe string IS present
    assert f"👤 <b>Имя:</b> {expected_safe_name}" in profile_html, "Escaped name not found in profile"

    print(f"\nSafe Profile HTML snippet:\n{profile_html}")
