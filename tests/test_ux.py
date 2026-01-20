import pytest
import os
import sys

# Ensure root is in path to pick up root gardarika package
sys.path.insert(0, os.getcwd())

from gardarika.ux import format_character_profile
from gardarika.character.attributes import Attribute
from gardarika.character.character import Character
from unittest.mock import MagicMock

# Helper to mock Character object
class MockCharacter:
    def __init__(self, name, class_name, faction_name):
        self.name = name
        self.level = 1
        self.health = 100
        self.mana = 50

        self.character_class = MagicMock()
        self.character_class.name = class_name

        self.faction = {'name': faction_name}

        self.attributes = {
            Attribute.STRENGTH: 10,
            Attribute.DEXTERITY: 10,
            Attribute.WISDOM: 10,
            Attribute.ENDURANCE: 10,
            Attribute.CHARISMA: 10,
        }

class MockRow:
    """Simulates sqlite3.Row behavior (subscriptable but not a dict)."""
    def __init__(self, data):
        self._data = data

    def __getitem__(self, key):
        return self._data[key]

def test_format_character_profile_dict():
    """Test formatting with a dictionary (simulating DB row)."""
    char_data = {
        'name': 'Ragnar',
        'class_name': 'Воин',
        'faction_name': 'Киев',
        'level': 5,
        'health': 150,
        'mana': 60,
        'strength': 15,
        'dexterity': 12,
        'wisdom': 8,
        'endurance': 14,
        'charisma': 10
    }

    output = format_character_profile(char_data)

    assert "👤 <b>Имя:</b> Ragnar" in output
    assert "🛡️ <b>Класс:</b> Воин" in output
    assert "💎 Сила: 15" in output
    assert "✨ Атрибуты:" in output

def test_format_character_profile_row():
    """Test formatting with a Row-like object."""
    data = {
        'name': 'Helga',
        'class_name': 'Волхв',
        'faction_name': 'Лес',
        'level': 2,
        'health': 80,
        'mana': 120,
        'strength': 5,
        'dexterity': 6,
        'wisdom': 15,
        'endurance': 8,
        'charisma': 12
    }
    row = MockRow(data)
    output = format_character_profile(row)

    assert "👤 <b>Имя:</b> Helga" in output
    assert "🛡️ <b>Класс:</b> Волхв" in output
    assert "🦉 Мудрость: 15" in output

def test_format_character_profile_object():
    """Test formatting with a Character-like object."""
    char_obj = MockCharacter('Lagertha', 'Охотник', 'Новгород')

    output = format_character_profile(char_obj)

    assert "👤 <b>Имя:</b> Lagertha" in output
    assert "🛡️ <b>Класс:</b> Охотник" in output
    assert "💎 Сила: 10" in output

def test_format_character_profile_escaping():
    """Test HTML escaping for user inputs."""
    char_data = {
        'name': '<b>Hacker</b>',
        'class_name': '<i>Mage</i>',
        'faction_name': 'Any',
    }

    output = format_character_profile(char_data)

    assert "&lt;b&gt;Hacker&lt;/b&gt;" in output
    assert "&lt;i&gt;Mage&lt;/i&gt;" in output

def test_character_str_integration():
    """Test that Character.__str__ uses format_character_profile."""
    # Use real character class
    char = Character("Bjorn", "воин", "novgorod")
    output = str(char)

    assert "👤 <b>Имя:</b> Bjorn" in output
    assert "🛡️ <b>Класс:</b> Воин" in output
    # Check for emoji from new implementation
    assert "💎" in output or "💪" not in output # Should contain diamond, not muscle (if we fully switched tokens)
    assert "✨" in output or "📜" in output
