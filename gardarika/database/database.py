# gardarika/database/database.py
import sqlite3

DATABASE_NAME = "gardarika.db"

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Инициализирует базу данных, создавая необходимые таблицы."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Создаем таблицу пользователей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,  -- Telegram User ID
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Создаем таблицу персонажей
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        name TEXT NOT NULL,
        class_name TEXT NOT NULL,
        faction_name TEXT NOT NULL,
        level INTEGER DEFAULT 1,
        experience INTEGER DEFAULT 0,
        health INTEGER NOT NULL,
        mana INTEGER NOT NULL,
        strength INTEGER NOT NULL,
        dexterity INTEGER NOT NULL,
        wisdom INTEGER NOT NULL,
        endurance INTEGER NOT NULL,
        charisma INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    conn.commit()
    conn.close()
    print("База данных успешно инициализирована.")

if __name__ == '__main__':
    # Этот блок выполнится, если запустить файл напрямую (python -m gardarika.database.database)
    # и создаст файл базы данных с нужными таблицами.
    initialize_database()
