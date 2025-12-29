# gardarika/character/character.py
from .classes import get_class
from ..lore.world import get_faction_info
from .attributes import (
    PrimaryAttribute,
    SecondaryAttribute,
    BASE_SECONDARY_ATTRIBUTES,
)

class Character:
    def __init__(self, name: str, character_class_name: str, faction_name: str):
        self.name = name

        # Устанавливаем класс и базовые первичные атрибуты
        self.character_class = get_class(character_class_name)
        if not self.character_class:
            raise ValueError(f"Неизвестный класс персонажа: {character_class_name}")

        self.primary_attributes = self.character_class.base_stats.copy()

        # Устанавливаем фракцию
        self.faction = get_faction_info(faction_name)
        if not self.faction:
            raise ValueError(f"Неизвестная фракция: {faction_name}")

        # Инициализируем вторичные атрибуты базовыми значениями
        self.secondary_attributes = BASE_SECONDARY_ATTRIBUTES.copy()

        # Начальные параметры
        self.level = 1
        self.experience = 0

        # Рассчитываем все вторичные характеристики
        self._calculate_secondary_attributes()

        # Здоровье и мана
        self.health = 100 + self.primary_attributes.get(PrimaryAttribute.ENDURANCE, 0) * 10
        self.mana = 50 + self.primary_attributes.get(PrimaryAttribute.WISDOM, 0) * 5

    def _calculate_secondary_attributes(self):
        """Рассчитывает вторичные характеристики на основе первичных."""
        pa = self.primary_attributes
        sa = self.secondary_attributes

        sa[SecondaryAttribute.PHYSICAL_DAMAGE] = round(5.0 + pa[PrimaryAttribute.STRENGTH] * 0.8 + pa[PrimaryAttribute.DEXTERITY] * 0.2, 1)
        sa[SecondaryAttribute.CRITICAL_CHANCE] = round(5.0 + pa[PrimaryAttribute.DEXTERITY] * 0.3, 1)
        sa[SecondaryAttribute.ARMOR_PENETRATION] = round(pa[PrimaryAttribute.STRENGTH] * 0.1, 1)
        sa[SecondaryAttribute.ATTACK_SPEED] = round(1.0 + pa[PrimaryAttribute.DEXTERITY] * 0.02, 2)
        sa[SecondaryAttribute.MAGIC_POWER] = round(pa[PrimaryAttribute.WISDOM] * 1.2, 1)
        sa[SecondaryAttribute.MAGIC_PENETRATION] = round(pa[PrimaryAttribute.WISDOM] * 0.1, 1)
        sa[SecondaryAttribute.ARMOR] = round(5.0 + pa[PrimaryAttribute.ENDURANCE] * 0.5 + pa[PrimaryAttribute.STRENGTH] * 0.2, 1)
        sa[SecondaryAttribute.MAGIC_RESIST] = round(5.0 + pa[PrimaryAttribute.WISDOM] * 0.4 + pa[PrimaryAttribute.ENDURANCE] * 0.2, 1)
        sa[SecondaryAttribute.EVASION] = round(5.0 + pa[PrimaryAttribute.DEXTERITY] * 0.4, 1)
        sa[SecondaryAttribute.HEALTH_REGEN] = round(1.0 + pa[PrimaryAttribute.ENDURANCE] * 0.1, 1)
        sa[SecondaryAttribute.MANA_REGEN] = round(0.5 + pa[PrimaryAttribute.WISDOM] * 0.05, 1)

    @classmethod
    def from_db_data(cls, db_row):
        """Создает экземпляр персонажа из данных базы данных."""
        # Создаем "пустой" экземпляр, передавая базовые данные
        instance = cls(db_row['name'], db_row['class_name'], db_row['faction_name'])

        # Перезаписываем первичные атрибуты и уровень данными из БД
        instance.level = db_row['level']
        instance.experience = db_row['experience']
        instance.primary_attributes = {
            PrimaryAttribute.STRENGTH: db_row['strength'],
            PrimaryAttribute.DEXTERITY: db_row['dexterity'],
            PrimaryAttribute.WISDOM: db_row['wisdom'],
            PrimaryAttribute.ENDURANCE: db_row['endurance'],
            PrimaryAttribute.CHARISMA: db_row['charisma'],
        }

        # Пересчитываем все на основе загруженных данных
        instance._calculate_secondary_attributes()
        instance.health = 100 + instance.primary_attributes.get(PrimaryAttribute.ENDURANCE, 0) * 10
        instance.mana = 50 + instance.primary_attributes.get(PrimaryAttribute.WISDOM, 0) * 5

        return instance

    def __str__(self):
        primary_attrs_str = "\n".join(f"  {attr.value}: {self.primary_attributes.get(attr, 0)}" for attr in PrimaryAttribute)

        secondary_attrs_str = (
            f"  <b>{SecondaryAttribute.PHYSICAL_DAMAGE.value}:</b> {self.secondary_attributes[SecondaryAttribute.PHYSICAL_DAMAGE]}\n"
            f"  <b>{SecondaryAttribute.CRITICAL_CHANCE.value}:</b> {self.secondary_attributes[SecondaryAttribute.CRITICAL_CHANCE]}%\n"
            f"  <b>{SecondaryAttribute.ARMOR_PENETRATION.value}:</b> {self.secondary_attributes[SecondaryAttribute.ARMOR_PENETRATION]}\n"
            f"  <b>{SecondaryAttribute.ATTACK_SPEED.value}:</b> {self.secondary_attributes[SecondaryAttribute.ATTACK_SPEED]}/сек\n\n"
            f"  <b>{SecondaryAttribute.MAGIC_POWER.value}:</b> {self.secondary_attributes[SecondaryAttribute.MAGIC_POWER]}\n"
            f"  <b>{SecondaryAttribute.MAGIC_PENETRATION.value}:</b> {self.secondary_attributes[SecondaryAttribute.MAGIC_PENETRATION]}\n\n"
            f"  <b>{SecondaryAttribute.ARMOR.value}:</b> {self.secondary_attributes[SecondaryAttribute.ARMOR]}\n"
            f"  <b>{SecondaryAttribute.MAGIC_RESIST.value}:</b> {self.secondary_attributes[SecondaryAttribute.MAGIC_RESIST]}\n"
            f"  <b>{SecondaryAttribute.EVASION.value}:</b> {self.secondary_attributes[SecondaryAttribute.EVASION]}%\n"
            f"  <b>{SecondaryAttribute.HEALTH_REGEN.value}:</b> {self.secondary_attributes[SecondaryAttribute.HEALTH_REGEN]}/сек\n"
            f"  <b>{SecondaryAttribute.MANA_REGEN.value}:</b> {self.secondary_attributes[SecondaryAttribute.MANA_REGEN]}/сек"
        )

        return (
            f"<b>Имя:</b> {self.name}\n"
            f"<b>Класс:</b> {self.character_class.name}\n"
            f"<b>Фракция:</b> {self.faction['name']}\n"
            f"<b>Уровень:</b> {self.level} (Опыт: {self.experience})\n"
            f"<b>Здоровье:</b> {self.health}\n"
            f"<b>Мана:</b> {self.mana}\n\n"
            f"--- <b>Первичные атрибуты</b> ---\n{primary_attrs_str}\n\n"
            f"--- <b>Боевые характеристики</b> ---\n{secondary_attrs_str}"
        )
