# gardarika/character/classes.py

from .attributes import PrimaryAttribute

BASE_STATS = {
    "Воин": {
        PrimaryAttribute.STRENGTH: 12,
        PrimaryAttribute.DEXTERITY: 8,
        PrimaryAttribute.WISDOM: 5,
        PrimaryAttribute.ENDURANCE: 10,
        PrimaryAttribute.CHARISMA: 7,
    },
    "Волхв": {
        PrimaryAttribute.STRENGTH: 5,
        PrimaryAttribute.DEXTERITY: 7,
        PrimaryAttribute.WISDOM: 12,
        PrimaryAttribute.ENDURANCE: 6,
        PrimaryAttribute.CHARISMA: 10,
    },
    "Охотник": {
        PrimaryAttribute.STRENGTH: 8,
        PrimaryAttribute.DEXTERITY: 12,
        PrimaryAttribute.WISDOM: 7,
        PrimaryAttribute.ENDURANCE: 8,
        PrimaryAttribute.CHARISMA: 6,
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
