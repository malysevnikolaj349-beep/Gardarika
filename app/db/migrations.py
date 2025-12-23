from app.db.database import Database


async def run_migrations(db: Database) -> None:
    await db.connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS dashboard_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            online INTEGER NOT NULL,
            economy_gold INTEGER NOT NULL,
            new_players INTEGER NOT NULL,
            server_load INTEGER NOT NULL,
            level_cap INTEGER NOT NULL,
            leader_name TEXT NOT NULL,
            leader_level INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seller TEXT NOT NULL,
            buyer TEXT NOT NULL,
            item TEXT NOT NULL,
            price INTEGER NOT NULL,
            deviation REAL NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS guild_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player TEXT NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS economy_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            auction_tax INTEGER NOT NULL,
            npc_buy_multiplier REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS world_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            time_mode TEXT NOT NULL,
            time_of_day TEXT NOT NULL,
            weather TEXT NOT NULL,
            season TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            nickname TEXT NOT NULL,
            level INTEGER NOT NULL,
            gold INTEGER NOT NULL,
            experience INTEGER NOT NULL,
            is_pk INTEGER NOT NULL,
            is_vip INTEGER NOT NULL,
            in_jail INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS inventories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            item TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS clans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            leader TEXT NOT NULL,
            treasury INTEGER NOT NULL,
            building_level INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS territories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mine TEXT NOT NULL,
            owner TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS action_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin TEXT NOT NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    await db.connection.commit()


async def seed_defaults(db: Database) -> None:
    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM dashboard_metrics")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.execute(
            """
            INSERT INTO dashboard_metrics (
                online, economy_gold, new_players, server_load, level_cap, leader_name, leader_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (124, 987654, 12, 8, 50, "Nagibator", 49),
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM trades")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO trades (seller, buyer, item, price, deviation, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                ("Veles", "Mila", "Секира Палача", 25000, 18.5, "pending"),
                ("Dobrynya", "Lada", "Чудотворный амулет", 99000, -12.0, "pending"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM guild_reports")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO guild_reports (player, reason, status)
            VALUES (?, ?, ?)
            """,
            [
                ("Varvara", "Слив цены", "open"),
                ("Karp", "РМТ подозрение", "open"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM economy_settings")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.execute(
            """
            INSERT INTO economy_settings (id, auction_tax, npc_buy_multiplier)
            VALUES (1, 5, 1.0)
            """
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM world_state")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.execute(
            """
            INSERT INTO world_state (id, time_mode, time_of_day, weather, season)
            VALUES (1, 'auto', 'day', 'clear', 'summer')
            """
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM events")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO events (name, status)
            VALUES (?, ?)
            """,
            [
                ("Нашествие Медведя", "ready"),
                ("Турнир Перуна", "ready"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM players")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO players (player_id, nickname, level, gold, experience, is_pk, is_vip, in_jail)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (101, "Stribog", 34, 12000, 44200, 0, 1, 0),
                (102, "Zorya", 12, 800, 3200, 0, 0, 1),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM inventories")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO inventories (player_id, item)
            VALUES (?, ?)
            """,
            [
                (101, "Именной меч"),
                (101, "Одержимый шлем"),
                (102, "Добротный лук"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM clans")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO clans (name, leader, treasury, building_level)
            VALUES (?, ?, ?, ?)
            """,
            [
                ("Острог Севера", "Stribog", 50000, 3),
                ("Громовники", "Perun", 78000, 4),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM territories")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO territories (mine, owner)
            VALUES (?, ?)
            """,
            [
                ("Серебряный рудник", "Острог Севера"),
                ("Медная шахта", "Громовники"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM quests")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO quests (name, status)
            VALUES (?, ?)
            """,
            [
                ("Летопись Мертвых", "active"),
                ("Гонка Наследия", "completed: Zorya"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM action_logs")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.executemany(
            """
            INSERT INTO action_logs (category, description)
            VALUES (?, ?)
            """,
            [
                ("combat", "Stribog победил медведя в (45, 12)"),
                ("loot", "Zorya подобрала Добротный лук"),
                ("trade", "Veles передал 500 золота Mila"),
            ],
        )

    cursor = await db.connection.execute("SELECT COUNT(*) as count FROM admin_logs")
    if (await cursor.fetchone())["count"] == 0:
        await db.connection.execute(
            """
            INSERT INTO admin_logs (admin, action, created_at)
            VALUES ('SYSTEM', 'Initial seed', '2024-01-01T00:00:00')
            """
        )

    await db.connection.commit()
