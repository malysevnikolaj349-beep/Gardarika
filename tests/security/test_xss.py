import unittest
import html
from gardarika.character.character import Character
from unittest.mock import patch, MagicMock

# Assuming these are available or mocked
# If get_class or get_faction_info fail, we might need to mock them.
# Let's check if we can import them.

class TestXSS(unittest.TestCase):
    def test_character_str_xss(self):
        """Test that Character.__str__ escapes HTML in the name."""
        malicious_name = "<b>Hacker</b>"

        # We need to ensure valid class and faction are passed if they are checked
        # Looking at previous test output, "воин" and "kiev" (or similar) seem to work.
        # But wait, character.py calls get_class("воин") etc.
        # If the environment is not set up correctly, this might fail.
        # However, since previous python3 test_xss.py worked, it means dependencies are there.

        try:
            char = Character(malicious_name, "воин", "kiev")
            output = str(char)

            # The output should contain the escaped version, not the raw tags
            self.assertIn(html.escape(malicious_name), output)
            self.assertNotIn(malicious_name, output) # "<b>Hacker</b>" shouldn't be there as is (unless escaped matches raw which it doesn't)

            # Specifically check for &lt;b&gt;
            self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", output)

        except Exception as e:
            self.fail(f"Character instantiation failed: {e}")

if __name__ == '__main__':
    unittest.main()
