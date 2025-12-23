from app.db.database import Database
from app.schemas.admin import EconomySettings, GuildReport, PendingTrade


class EconomyService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def list_pending_trades(self) -> list[PendingTrade]:
        cursor = await self.db.connection.execute(
            "SELECT id, seller, buyer, item, price, deviation, status FROM trades WHERE status = 'pending'"
        )
        rows = await cursor.fetchall()
        return [PendingTrade(**row) for row in rows]

    async def update_trade_status(self, trade_id: int, status: str) -> None:
        await self.db.connection.execute(
            "UPDATE trades SET status = ? WHERE id = ?", (status, trade_id)
        )
        await self.db.connection.commit()

    async def list_guild_reports(self) -> list[GuildReport]:
        cursor = await self.db.connection.execute(
            "SELECT id, player, reason, status FROM guild_reports"
        )
        rows = await cursor.fetchall()
        return [GuildReport(**row) for row in rows]

    async def update_guild_report(self, report_id: int, status: str) -> None:
        await self.db.connection.execute(
            "UPDATE guild_reports SET status = ? WHERE id = ?", (status, report_id)
        )
        await self.db.connection.commit()

    async def get_settings(self) -> EconomySettings:
        cursor = await self.db.connection.execute(
            "SELECT auction_tax, npc_buy_multiplier FROM economy_settings WHERE id = 1"
        )
        row = await cursor.fetchone()
        if not row:
            return EconomySettings()
        return EconomySettings(**row)

    async def update_settings(self, auction_tax: int, npc_buy_multiplier: float) -> EconomySettings:
        await self.db.connection.execute(
            """
            INSERT INTO economy_settings (id, auction_tax, npc_buy_multiplier)
            VALUES (1, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                auction_tax = excluded.auction_tax,
                npc_buy_multiplier = excluded.npc_buy_multiplier
            """,
            (auction_tax, npc_buy_multiplier),
        )
        await self.db.connection.commit()
        return await self.get_settings()
