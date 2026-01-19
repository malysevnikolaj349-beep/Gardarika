import html
from gardarika.character.attributes import Attribute

# Emoji Design Tokens
ICON_NAME = "👤"
ICON_CLASS = "🛡️"
ICON_FACTION = "🚩"
ICON_LEVEL = "📊"
ICON_HEALTH = "❤️"
ICON_MANA = "💧"
ICON_PROFILE_HEADER = "📜"
ICON_ATTRIBUTES_HEADER = "✨"

# Attribute Icons
ICON_STRENGTH = "💎"
ICON_DEXTERITY = "🧶"
ICON_WISDOM = "🦉"
ICON_ENDURANCE = "🐎"
ICON_CHARISMA = "🎭"

ATTRIBUTE_ICONS = {
    Attribute.STRENGTH: ICON_STRENGTH,
    Attribute.DEXTERITY: ICON_DEXTERITY,
    Attribute.WISDOM: ICON_WISDOM,
    Attribute.ENDURANCE: ICON_ENDURANCE,
    Attribute.CHARISMA: ICON_CHARISMA,
}


def format_character_profile(
    name: str,
    class_name: str,
    faction_name: str,
    level: int,
    experience: int,
    health: int,
    mana: int,
    attributes: dict
) -> str:
    """
    Formats the character profile with standardized emojis and HTML escaping.
    Accepts attributes dict keyed by Attribute enum, english string keys,
    or Russian labels.
    """
    safe_name = html.escape(str(name))
    safe_class = html.escape(str(class_name))
    safe_faction = html.escape(str(faction_name))

    # Helper to resolve attribute value from various key formats
    def get_val(attr_enum, eng_key):
        return (
            attributes.get(attr_enum) or
            attributes.get(eng_key) or
            attributes.get(attr_enum.value, 0)
        )

    str_val = get_val(Attribute.STRENGTH, 'strength')
    dex_val = get_val(Attribute.DEXTERITY, 'dexterity')
    wis_val = get_val(Attribute.WISDOM, 'wisdom')
    end_val = get_val(Attribute.ENDURANCE, 'endurance')
    cha_val = get_val(Attribute.CHARISMA, 'charisma')

    return (
        f"{ICON_PROFILE_HEADER} <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        f"{ICON_NAME} <b>Имя:</b> {safe_name}\n"
        f"{ICON_CLASS} <b>Класс:</b> {safe_class}\n"
        f"{ICON_FACTION} <b>Фракция:</b> {safe_faction}\n"
        f"{ICON_LEVEL} <b>Уровень:</b> {level} (Опыт: {experience})\n"
        f"{ICON_HEALTH} <b>Здоровье:</b> {health} "
        f"| {ICON_MANA} <b>Мана:</b> {mana}\n\n"
        f"<b>{ICON_ATTRIBUTES_HEADER} Атрибуты:</b>\n"
        f"  {ICON_STRENGTH} Сила: {str_val}\n"
        f"  {ICON_DEXTERITY} Ловкость: {dex_val}\n"
        f"  {ICON_WISDOM} Мудрость: {wis_val}\n"
        f"  {ICON_ENDURANCE} Выносливость: {end_val}\n"
        f"  {ICON_CHARISMA} Харизма: {cha_val}"
    )
