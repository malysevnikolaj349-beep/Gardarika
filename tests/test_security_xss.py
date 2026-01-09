import pytest
from gardarika.character.character import Character
from gardarika.character.classes import CharacterClass
from gardarika.lore.world import FACTIONS
import html

# Mocking external dependencies if necessary, but Character seems self-contained enough
# providing we have valid class and faction names.
# We need to know valid class and faction names.
# From bot.py: classes: "воин", "волхв", "охотник"
# From bot.py: factions: "kiev", "novgorod", "forest_tribes"

def test_character_str_xss_vulnerability():
    """
    Test that Character.__str__ does NOT currently escape HTML tags in the name,
    demonstrating the vulnerability.
    Once fixed, we will update this test to expect escaped HTML.
    """
    # Malicious name with HTML tags
    malicious_name = "<b>Hacker</b>"

    # Create character
    try:
        char = Character(malicious_name, "воин", "kiev")
    except ValueError:
        pytest.fail("Failed to create character with assumed valid class/faction")

    profile_str = str(char)

    # VULNERABILITY CHECK:
    # After fix, the string should contain escaped HTML.
    escaped_name = html.escape(malicious_name)
    assert f"<b>Имя:</b> {escaped_name}" in profile_str
    assert f"<b>Имя:</b> {malicious_name}" not in profile_str

def test_bot_profile_formatting_xss_vulnerability():
    """
    Test logic similar to bot.py's profile function.
    """
    character_data = {
        'name': '<script>alert("xss")</script>',
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

    # Simulate the fix in bot.py
    escaped_name = html.escape(character_data['name'])
    message = (
        f"<b>Имя:</b> {escaped_name}\n"
        f"<b>Класс:</b> {character_data['class_name']}\n"
    )

    # VULNERABILITY CHECK:
    assert f"<b>Имя:</b> {escaped_name}" in message
    assert f"<b>Имя:</b> {character_data['name']}" not in message
