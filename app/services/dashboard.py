from app.db.database import Database
from app.schemas.admin import DashboardStats


class DashboardService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def get_stats(self) -> DashboardStats:
        cursor = await self.db.connection.execute(
            "SELECT online, economy_gold, new_players, server_load, level_cap, leader_name, leader_level FROM dashboard_metrics LIMIT 1"
        )
        row = await cursor.fetchone()
        return DashboardStats(**row)

    async def force_new_epoch(self) -> DashboardStats:
        await self.db.connection.execute(
            "UPDATE dashboard_metrics SET level_cap = level_cap + 10"
        )
        await self.db.connection.commit()
        return await self.get_stats()
