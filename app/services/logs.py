from datetime import datetime

from app.db.database import Database
from app.schemas.admin import ActionLog, AdminLog


class LogService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def list_action_logs(self) -> list[ActionLog]:
        cursor = await self.db.connection.execute(
            "SELECT id, category, description FROM action_logs ORDER BY id DESC LIMIT 50"
        )
        rows = await cursor.fetchall()
        return [ActionLog(**row) for row in rows]

    async def list_admin_logs(self) -> list[AdminLog]:
        cursor = await self.db.connection.execute(
            "SELECT id, admin, action, created_at FROM admin_logs ORDER BY id DESC LIMIT 50"
        )
        rows = await cursor.fetchall()
        return [AdminLog(**row) for row in rows]

    async def add_admin_log(self, admin: str, action: str) -> None:
        await self.db.connection.execute(
            "INSERT INTO admin_logs (admin, action, created_at) VALUES (?, ?, ?)",
            (admin, action, datetime.utcnow().isoformat()),
        )
        await self.db.connection.commit()
