import html
from gardarika.character.attributes import Attribute

# Standardized Emoji Design Tokens
EMOJI_TOKENS = {
    "name": "👤",
    "class": "🛡️",
    "faction": "🚩",
    "level": "📊",
    "health": "❤️",
    "mana": "💧",
    "strength": "💎",
    "dexterity": "🧶",
    "wisdom": "🦉",
    "endurance": "🐎",
    "charisma": "🎭",
    "profile_header": "📜",
    "attributes_header": "✨",
}

def format_character_profile(character_data):
    """
    Formats a character profile for display in Telegram.
    Accepts a dictionary-like object (dict or sqlite3.Row) or a Character instance.
    """
    # Helper to safe get attribute, handling both object and dict access
    def get_val(obj, key, default=None):
        try:
            return obj[key]
        except (KeyError, TypeError, IndexError, AttributeError):
            return getattr(obj, key, default)

    # Helper to get attribute value from attributes dict or direct keys
    def get_attr(obj, attr_enum, key_str):
        # Try retrieving from 'attributes' dict first (Character object structure)
        attrs = get_val(obj, 'attributes')
        if attrs and isinstance(attrs, dict):
            return attrs.get(attr_enum, 0)

        # Fallback to direct key access (DB row structure)
        return get_val(obj, key_str, 0)

    name = html.escape(str(get_val(character_data, 'name', 'Неизвестно')))

    # Handle class name
    class_name = get_val(character_data, 'class_name')
    if not class_name:
         # Try accessing nested object property if it's a Character instance
         char_class = get_val(character_data, 'character_class')
         if char_class:
             class_name = char_class.name
    class_name = html.escape(str(class_name or 'Неизвестно'))

    # Handle faction name
    faction_name = get_val(character_data, 'faction_name')
    if not faction_name:
         faction = get_val(character_data, 'faction')
         if faction and isinstance(faction, dict):
             faction_name = faction.get('name')
    faction_name = html.escape(str(faction_name or 'Неизвестно'))

    level = get_val(character_data, 'level', 1)
    health = get_val(character_data, 'health', 0)
    mana = get_val(character_data, 'mana', 0)

    str_val = get_attr(character_data, Attribute.STRENGTH, 'strength')
    dex_val = get_attr(character_data, Attribute.DEXTERITY, 'dexterity')
    wis_val = get_attr(character_data, Attribute.WISDOM, 'wisdom')
    end_val = get_attr(character_data, Attribute.ENDURANCE, 'endurance')
    cha_val = get_attr(character_data, Attribute.CHARISMA, 'charisma')

    return (
        f"{EMOJI_TOKENS['profile_header']} <b>ПРОФИЛЬ ГЕРОЯ</b>\n\n"
        f"{EMOJI_TOKENS['name']} <b>Имя:</b> {name}\n"
        f"{EMOJI_TOKENS['class']} <b>Класс:</b> {class_name}\n"
        f"{EMOJI_TOKENS['faction']} <b>Фракция:</b> {faction_name}\n"
        f"{EMOJI_TOKENS['level']} <b>Уровень:</b> {level}\n"
        f"{EMOJI_TOKENS['health']} <b>Здоровье:</b> {health}\n"
        f"{EMOJI_TOKENS['mana']} <b>Мана:</b> {mana}\n\n"
        f"<b>{EMOJI_TOKENS['attributes_header']} Атрибуты:</b>\n"
        f"  {EMOJI_TOKENS['strength']} Сила: {str_val}\n"
        f"  {EMOJI_TOKENS['dexterity']} Ловкость: {dex_val}\n"
        f"  {EMOJI_TOKENS['wisdom']} Мудрость: {wis_val}\n"
        f"  {EMOJI_TOKENS['endurance']} Выносливость: {end_val}\n"
        f"  {EMOJI_TOKENS['charisma']} Харизма: {cha_val}"
    )
