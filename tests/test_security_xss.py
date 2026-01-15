import pytest
from gardarika.character.character import Character
from unittest.mock import MagicMock, patch

# Mock dependencies since we just want to test __str__
@patch('gardarika.character.character.get_class')
@patch('gardarika.character.character.get_faction_info')
def test_character_str_xss_vulnerability(mock_get_faction, mock_get_class):
    # Setup mocks
    mock_class = MagicMock()
    mock_class.name = "Warrior"
    mock_class.base_stats = {'STRENGTH': 10}
    mock_get_class.return_value = mock_class

    mock_faction = {'name': "Kiev"}
    mock_get_faction.return_value = mock_faction

    # Malicious input
    malicious_name = "<b>Hacker</b>"

    char = Character(malicious_name, "warrior", "kiev")

    # Check if the output contains the raw malicious tag (vulnerable)
    # or escaped version (secure)
    output = str(char)

    # We want to assertion to FAIL if it IS vulnerable, or pass if it IS vulnerable?
    # Usually I write a test that asserts the CORRECT behavior (secure).
    # So if it's currently vulnerable, this test should fail.

    assert "&lt;b&gt;Hacker&lt;/b&gt;" in output, "Character name is not escaped in __str__ output!"
    assert "<b>Hacker</b>" not in output, "Raw HTML tags found in __str__ output!"
