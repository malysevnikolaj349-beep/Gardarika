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

