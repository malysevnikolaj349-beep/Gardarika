# gardarika/character/classes.py

from .attributes import Attribute

BASE_STATS = {
    "Воин": {
        Attribute.STRENGTH: 12,
        Attribute.DEXTERITY: 8,
        Attribute.WISDOM: 5,
        Attribute.ENDURANCE: 10,
        Attribute.CHARISMA: 7,
    },
    "Волхв": {
        Attribute.STRENGTH: 5,
        Attribute.DEXTERITY: 7,
        Attribute.WISDOM: 12,
        Attribute.ENDURANCE: 6,
        Attribute.CHARISMA: 10,
    },
    "Охотник": {
        Attribute.STRENGTH: 8,
        Attribute.DEXTERITY: 12,
        Attribute.WISDOM: 7,
        Attribute.ENDURANCE: 8,
        Attribute.CHARISMA: 6,
    }
}

class CharacterClass:
    def __init__(self, name, description, base_stats):
        self.name = name
        self.description = description
        self.base_stats = base_stats

    def __str__(self):
        return self.name

# Создаем экземпляры классов
WARRIOR = CharacterClass(
    "Воин",
    "Мастер ближнего боя, полагающийся на силу и выносливость.",
    BASE_STATS["Воин"]
)

MAGE = CharacterClass(
    "Волхв",
    "Мудрец, черпающий силу из древних знаний и связи с миром духов.",
    BASE_STATS["Волхв"]
)

HUNTER = CharacterClass(
    "Охотник",
    "Ловкий и незаметный следопыт, мастер дальнего боя и выживания в дикой природе.",
    BASE_STATS["Охотник"]
)

AVAILABLE_CLASSES = {
    "воин": WARRIOR,
    "волхв": MAGE,
    "охотник": HUNTER
}

def get_class(class_name):
    """Возвращает экземпляр класса персонажа по его названию."""
    return AVAILABLE_CLASSES.get(class_name.lower())
