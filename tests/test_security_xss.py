import pytest
from gardarika.character.character import Character
from unittest.mock import MagicMock
import html

# Mock dependencies if needed, but Character class seems self-contained enough
# except for database lookups in __init__ which we might need to mock or ensure exist.
# Character.__init__ calls get_class and get_faction_info.

def test_character_str_xss_protection():
    """
    Test that the Character.__str__ method escapes HTML in the character name.
    """
    # We need to ensure valid class and faction names are used so __init__ doesn't fail.
    # Based on bot.py: class='воин', faction='kiev' (or whatever the keys are).
    # Let's check bot.py/available classes.

    # We'll use a mock for the dependencies to avoid DB/Module coupling if possible,
    # but Character logic is tight.
    # Let's assume 'warrior' and 'kiev' might work or we check available classes.
    # Actually, we can just mock the whole class/faction objects if we can't instantiate.

    # However, let's try to instantiate with what we think are valid values.
    # If that fails, we will mock get_class and get_faction_info.

    # Looking at bot.py:
    # classes: "воин", "волхв", "охотник" -> these are keys in AVAILABLE_CLASSES presumably.
    # factions: "kiev", "novgorod", "forest_tribes" -> keys in FACTIONS.

    # We need to make sure we can import Character and it works.

    malicious_name = "<b>Bold</b> & <script>alert('XSS')</script>"

    # We might need to mock gardarika.character.classes.get_class and gardarika.lore.world.get_faction_info
    # because we don't know if the data files are present or DB is needed.
    # Character.__init__ calls them.

    try:
        # Attempting to use real classes if they exist in code
        char = Character(malicious_name, "воин", "kiev")
    except Exception:
        # If real instantiation fails due to missing data/db, we mock.
        pass

    # Re-defining with mocks to be safe and isolated
    # We need to patch where Character imports them.

    from unittest.mock import patch

    with patch("gardarika.character.character.get_class") as mock_get_class, \
         patch("gardarika.character.character.get_faction_info") as mock_get_faction:

        # Setup mocks
        mock_class = MagicMock()
        mock_class.name = "Warrior"
        mock_class.base_stats = {}
        mock_get_class.return_value = mock_class

        mock_faction = MagicMock()
        mock_faction.__getitem__.return_value = "Kiev" # for faction['name']
        mock_get_faction.return_value = mock_faction

        char = Character(malicious_name, "some_class", "some_faction")

        output = str(char)

        # We expect the name to be escaped
        expected_name = html.escape(malicious_name)

        assert expected_name in output
        assert "<script>" not in output # Should be &lt;script&gt;
        assert "<b>Bold</b>" not in output # Should be &lt;b&gt;Bold&lt;/b&gt;
