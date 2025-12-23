from app.db.database import Database
from app.schemas.admin import ClanSummary, TerritorySummary


class ClanService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def list_clans(self) -> list[ClanSummary]:
        cursor = await self.db.connection.execute(
            "SELECT id, name, leader, treasury, building_level FROM clans"
        )
        rows = await cursor.fetchall()
        return [ClanSummary(**row) for row in rows]

    async def update_leader(self, clan_id: int, leader: str) -> None:
        await self.db.connection.execute(
            "UPDATE clans SET leader = ? WHERE id = ?", (leader, clan_id)
        )
        await self.db.connection.commit()

    async def list_territories(self) -> list[TerritorySummary]:
        cursor = await self.db.connection.execute(
            "SELECT id, mine, owner FROM territories"
        )
        rows = await cursor.fetchall()
        return [TerritorySummary(**row) for row in rows]

    async def reset_territories(self) -> None:
        await self.db.connection.execute("UPDATE territories SET owner = 'Свободно'")
        await self.db.connection.commit()
