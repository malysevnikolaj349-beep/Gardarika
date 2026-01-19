from .classes import get_class
from .attributes import Attribute
from ..lore.world import get_faction_info
from ..ux import format_character_profile


class Character:
    def __init__(self, name, character_class_name, faction_name):
        self.name = name

        # Устанавливаем класс и базовые атрибуты
        self.character_class = get_class(character_class_name)
        if not self.character_class:
            raise ValueError(
                f"Неизвестный класс персонажа: {character_class_name}"
            )

        self.attributes = self.character_class.base_stats.copy()

        # Устанавливаем фракцию
        self.faction = get_faction_info(faction_name)
        if not self.faction:
            raise ValueError(f"Неизвестная фракция: {faction_name}")

        # Начальные параметры
        self.level = 1
        self.experience = 0
        self.health = 100 + self.attributes.get(Attribute.ENDURANCE, 0)
        self.mana = 50 + self.attributes.get(Attribute.WISDOM, 0)

    def __str__(self):
        return format_character_profile(
            name=self.name,
            class_name=self.character_class.name,
            faction_name=self.faction['name'],
            level=self.level,
            experience=self.experience,
            health=self.health,
            mana=self.mana,
            attributes=self.attributes
        )
