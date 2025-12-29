# gardarika/database/operations.py
from .database import get_db_connection

def add_user_if_not_exists(user_id: int):
    """Добавляет нового пользователя в базу данных, если он еще не существует."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_character_by_user_id(user_id: int):
    """Возвращает данные персонажа по ID пользователя Telegram."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE user_id = ?", (user_id,))
    character_data = cursor.fetchone()
    conn.close()
    return character_data

def create_character(user_id: int, name: str, class_name: str, faction_name: str, stats: dict):
    """Создает нового персонажа и сохраняет его в базу данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO characters (user_id, name, class_name, faction_name, health, mana,
                                strength, dexterity, wisdom, endurance, charisma)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, name, class_name, faction_name, stats['health'], stats['mana'],
         stats['strength'], stats['dexterity'], stats['wisdom'], stats['endurance'], stats['charisma'])
    )
    conn.commit()
    conn.close()
