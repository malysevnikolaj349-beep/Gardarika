from .character.attributes import Attribute

# --- Emoji Design Tokens ---
ICON_PROFILE = "📜"
ICON_NAME = "👤"
ICON_CLASS = "🛡"
ICON_FACTION = "🚩"
ICON_LEVEL = "📊"
ICON_HEALTH = "❤️"
ICON_MANA = "💧"
ICON_ATTRIBUTES = "💎"
ICON_STRENGTH = "💪"
ICON_DEXTERITY = "🦶"
ICON_WISDOM = "🦉"
ICON_ENDURANCE = "🐎"
ICON_CHARISMA = "🎭"


def format_character_profile(data) -> str:
    """
    Форматирует профиль персонажа в HTML строку с использованием эмодзи.
    Принимает либо объект Character, либо словарь/sqlite3.Row.
    """
    # Определяем, откуда брать данные
    if hasattr(data, 'character_class'):
        # Это объект Character
        name = data.name
        class_name = data.character_class.name
        faction_name = data.faction['name']
        level = data.level
        experience = getattr(data, 'experience', 0)
        health = data.health
        mana = data.mana

        # Атрибуты хранятся в dict с Enum ключами
        attrs = data.attributes
        strength = attrs.get(Attribute.STRENGTH, 0)
        dexterity = attrs.get(Attribute.DEXTERITY, 0)
        wisdom = attrs.get(Attribute.WISDOM, 0)
        endurance = attrs.get(Attribute.ENDURANCE, 0)
        charisma = attrs.get(Attribute.CHARISMA, 0)

    else:
        # Это словарь или sqlite3.Row
        def get_val(key):
            if isinstance(data, dict):
                return data.get(key, 0)
            try:
                # Для sqlite3.Row
                return data[key]
            except (IndexError, KeyError, TypeError):
                return 0

        name = get_val('name')
        class_name = get_val('class_name')
        faction_name = get_val('faction_name')
        level = get_val('level')
        experience = get_val('experience')
        health = get_val('health')
        mana = get_val('mana')
        strength = get_val('strength')
        dexterity = get_val('dexterity')
        wisdom = get_val('wisdom')
        endurance = get_val('endurance')
        charisma = get_val('charisma')

    # Формируем строку
    # Добавляем опыт к уровню, если он есть
    level_str = f"{level}"
    if experience > 0:
        level_str += f" (Опыт: {experience})"

    return (
        f"{ICON_PROFILE} <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        f"{ICON_NAME} <b>Имя:</b> {name}\n"
        f"{ICON_CLASS} <b>Класс:</b> {class_name}\n"
        f"{ICON_FACTION} <b>Фракция:</b> {faction_name}\n"
        f"{ICON_LEVEL} <b>Уровень:</b> {level_str}\n"
        f"{ICON_HEALTH} <b>Здоровье:</b> {health} | {ICON_MANA} <b>Мана:</b> {mana}\n\n"
        f"<b>{ICON_ATTRIBUTES} Атрибуты:</b>\n"
        f"  {ICON_STRENGTH} Сила: {strength}\n"
        f"  {ICON_DEXTERITY} Ловкость: {dexterity}\n"
        f"  {ICON_WISDOM} Мудрость: {wisdom}\n"
        f"  {ICON_ENDURANCE} Выносливость: {endurance}\n"
        f"  {ICON_CHARISMA} Харизма: {charisma}"
    )
