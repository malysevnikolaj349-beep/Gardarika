from app.db.database import Database
from app.schemas.admin import QuestStatus


class ContentService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def list_quests(self) -> list[QuestStatus]:
        cursor = await self.db.connection.execute("SELECT id, name, status FROM quests")
        rows = await cursor.fetchall()
        return [QuestStatus(**row) for row in rows]

    async def reset_legend(self, quest_id: int) -> None:
        await self.db.connection.execute(
            "UPDATE quests SET status = 'active' WHERE id = ?", (quest_id,)
        )
        await self.db.connection.commit()

    async def spawn_item(self, player_id: int, item: str) -> None:
        await self.db.connection.execute(
            "INSERT INTO inventories (player_id, item) VALUES (?, ?)", (player_id, item)
        )
        await self.db.connection.commit()
