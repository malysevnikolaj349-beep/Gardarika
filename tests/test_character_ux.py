import html
import sys
import os

# Insert root directory to sys.path to ensure we test the root package code
sys.path.insert(0, os.path.abspath("."))  # noqa: E402

from gardarika.character.character import Character  # noqa: E402


def test_character_str_formatting_and_escaping():
    # Setup
    name = "<b>Ivan</b> & Mary"
    class_key = "воин"
    faction_key = "novgorod"

    # Create Character
    char = Character(name, class_key, faction_key)

    # Render string
    output = str(char)

    # Verify Escaping
    assert "<b>Ivan</b>" not in output
    assert html.escape(name) in output

    # Verify Emojis
    assert "📜" in output
    assert "👤" in output
    assert "🛡️" in output
    assert "🚩" in output
    assert "📊" in output
    assert "❤️" in output
    assert "💧" in output
    assert "✨" in output
    assert "💎" in output
    assert "🧶" in output
    assert "🦉" in output
    assert "🐎" in output
    assert "🎭" in output

    # Verify Data
    assert "Воин" in output
    assert "Новгородская Республика" in output
