# gardarika/character/character.py

import html
from .classes import get_class
from .attributes import Attribute
from ..lore.world import get_faction_info

class Character:
    def __init__(self, name, character_class_name, faction_name):
        self.name = name

        # Устанавливаем класс и базовые атрибуты
        self.character_class = get_class(character_class_name)
        if not self.character_class:
            raise ValueError(f"Неизвестный класс персонажа: {character_class_name}")

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
        return (
            f"📜 <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
            f"👤 <b>Имя:</b> {html.escape(self.name)}\n"
            f"🛡️ <b>Класс:</b> {self.character_class.name}\n"
            f"🚩 <b>Фракция:</b> {self.faction['name']}\n"
            f"📊 <b>Уровень:</b> {self.level}\n"
            f"❤️ <b>Здоровье:</b> {self.health}\n"
            f"💧 <b>Мана:</b> {self.mana}\n\n"
            f"<b>💎 Атрибуты:</b>\n"
            f"  💪 Сила: {self.attributes.get(Attribute.STRENGTH, 0)}\n"
            f"  🧶 Ловкость: {self.attributes.get(Attribute.DEXTERITY, 0)}\n"
            f"  🦉 Мудрость: {self.attributes.get(Attribute.WISDOM, 0)}\n"
            f"  🐴 Выносливость: {self.attributes.get(Attribute.ENDURANCE, 0)}\n"
            f"  🎭 Харизма: {self.attributes.get(Attribute.CHARISMA, 0)}"
        )
