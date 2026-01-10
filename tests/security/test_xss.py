import unittest
from gardarika.character.character import Character

class TestXSS(unittest.TestCase):
    def test_character_str_escapes_html(self):
        # Create a character with a name containing HTML tags
        malicious_name = "<b>Hacker</b>"

        try:
            char = Character(malicious_name, "воин", "kiev")
            output = str(char)

            # The current implementation DOES NOT escape, so this test should fail if I assert it DOES escape.
            # I want to verify the vulnerability first.

            # Vulnerability verification:
            # If the output contains the raw malicious string "<b>Hacker</b>", it means it's NOT escaped.
            # Note that "<b>Name:</b>" is part of the template, so "<b>Hacker</b>" will appear as the value.
            # The template is: f"👤 <b>Имя:</b> {self.name}\n"
            # So output will have: "👤 <b>Имя:</b> <b>Hacker</b>\n"

            print(f"DEBUG: Output is: {output}")

            # Assertion for DESIRED behavior (Security Fix):
            # It should be escaped to "&lt;b&gt;Hacker&lt;/b&gt;" in the output string
            # (or at least not raw tags).

            # Since I am fixing it, I will assert the SAFE behavior.
            # This test is expected to FAIL currently.

            self.assertIn("&lt;b&gt;Hacker&lt;/b&gt;", output, "Character name with HTML tags was not escaped!")
            self.assertNotIn("<b>Hacker</b>", output.replace("<b>Имя:</b> ", ""), "Raw HTML tags found in user input!")

        except ValueError as e:
            self.fail(f"Could not create character: {e}")
        except Exception as e:
            self.fail(f"An error occurred: {e}")

if __name__ == "__main__":
    unittest.main()
