import pytest
import os
import sys

# Ensure root directory is in path
sys.path.insert(0, os.path.abspath("."))

from gardarika.character.character import Character

def test_character_str_html_injection():
    """
    Test that Character.__str__ DOES escape HTML in the name,
    fixing the vulnerability.
    """
    name_with_html = "<b>BoldName</b>"
    char = Character(name_with_html, "воин", "kiev")
    output = str(char)

    # Secure behavior: The tag should be escaped
    assert "&lt;b&gt;BoldName&lt;/b&gt;" in output
    assert "<b>BoldName</b>" not in output
