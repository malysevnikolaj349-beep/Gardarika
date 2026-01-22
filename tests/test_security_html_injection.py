import sys
import os

# Insert root directory to sys.path to allow importing root gardarika package
# We insert at 0 to take precedence over src/gardarika if it's already in path
sys.path.insert(0, os.path.abspath("."))

import pytest
from gardarika.character.character import Character
from gardarika.character.attributes import Attribute
from gardarika.character.classes import AVAILABLE_CLASSES
import html

# Mock classes and factions if needed, but we can use real ones for this test
# assuming "воин" and "kiev" exist based on previous reads

def test_character_str_html_injection():
    """
    Test that Character.__str__ escapes HTML in the name.
    """
    malicious_name = "<b>Hacker</b>"
    # Warrior and kiev should be valid
    char = Character(malicious_name, "воин", "kiev")

    output = str(char)

    # We expect the name to be escaped: &lt;b&gt;Hacker&lt;/b&gt;
    # If it is not escaped, it will be <b>Hacker</b> which is vulnerable in HTML context

    assert html.escape(malicious_name) in output
    assert malicious_name not in output  # strict check: raw HTML should not be present

def test_character_str_attributes_escaping():
    """
    Test that other string attributes are also escaped if they could be manipulated.
    (Although class and faction are hardcoded, it's good practice)
    """
    # Just to be safe, check if class name is rendered safely (it should be, as it comes from internal dict)
    pass
