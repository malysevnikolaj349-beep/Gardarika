# gardarika/character/attributes.py
from enum import Enum

class PrimaryAttribute(Enum):
    """Первичные атрибуты, которые игрок может повышать с уровнем."""
    STRENGTH = "Сила"
    DEXTERITY = "Ловкость"
    WISDOM = "Мудрость"
    ENDURANCE = "Выносливость"
    CHARISMA = "Харизма"

class SecondaryAttribute(Enum):
    """
    Вторичные (боевые) характеристики, которые рассчитываются на основе
    первичных атрибутов, класса, уровня и экипировки.
    """
    # Физические атаки
    PHYSICAL_DAMAGE = "Физический урон"
    ARMOR_PENETRATION = "Пробитие брони"
    CRITICAL_CHANCE = "Шанс крит. удара"
    CRITICAL_DAMAGE = "Крит. урон"
    ATTACK_SPEED = "Скорость атаки"

    # Магические атаки
    MAGIC_POWER = "Магическая сила"
    MAGIC_PENETRATION = "Маг. пробитие"
    COOLDOWN_REDUCTION = "Снижение перезарядки"

    # Защита
    ARMOR = "Броня"
    MAGIC_RESIST = "Сопротивление магии"
    HEALTH_REGEN = "Регенерация здоровья"
    MANA_REGEN = "Регенерация маны"
    EVASION = "Уклонение"

# Для удобства создадим словари с начальными значениями
# Вторичные характеристики по умолчанию начинаются с базовых значений
BASE_SECONDARY_ATTRIBUTES = {
    SecondaryAttribute.PHYSICAL_DAMAGE: 5.0,
    SecondaryAttribute.ARMOR_PENETRATION: 0.0,
    SecondaryAttribute.CRITICAL_CHANCE: 5.0,  # в процентах
    SecondaryAttribute.CRITICAL_DAMAGE: 150.0, # в процентах
    SecondaryAttribute.ATTACK_SPEED: 1.0,    # атак в секунду
    SecondaryAttribute.MAGIC_POWER: 0.0,
    SecondaryAttribute.MAGIC_PENETRATION: 0.0,
    SecondaryAttribute.COOLDOWN_REDUCTION: 0.0,
    SecondaryAttribute.ARMOR: 5.0,
    SecondaryAttribute.MAGIC_RESIST: 5.0,
    SecondaryAttribute.HEALTH_REGEN: 1.0,    # в секунду
    SecondaryAttribute.MANA_REGEN: 0.5,      # в секунду
    SecondaryAttribute.EVASION: 5.0          # в процентах
}
