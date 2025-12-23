from app.db.database import Database
from app.schemas.admin import PlayerProfile


class PlayerService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def find_player(self, query: str) -> PlayerProfile | None:
        if query.isdigit():
            cursor = await self.db.connection.execute(
                """
                SELECT player_id, nickname, level, gold, experience, is_pk, is_vip, in_jail
                FROM players
                WHERE player_id = ?
                """,
                (int(query),),
            )
        else:
            cursor = await self.db.connection.execute(
                """
                SELECT player_id, nickname, level, gold, experience, is_pk, is_vip, in_jail
                FROM players
                WHERE nickname LIKE ?
                """,
                (f"%{query}%",),
            )
        row = await cursor.fetchone()
        if not row:
            return None
        inventory_cursor = await self.db.connection.execute(
            "SELECT item FROM inventories WHERE player_id = ?", (row["player_id"],)
        )
        inventory_rows = await inventory_cursor.fetchall()
        return PlayerProfile(
            player_id=row["player_id"],
            nickname=row["nickname"],
            level=row["level"],
            gold=row["gold"],
            experience=row["experience"],
            is_pk=bool(row["is_pk"]),
            is_vip=bool(row["is_vip"]),
            in_jail=bool(row["in_jail"]),
            inventory=[item["item"] for item in inventory_rows],
        )

    async def update_player(
        self,
        player_id: int,
        level: int | None = None,
        gold: int | None = None,
        experience: int | None = None,
        is_pk: bool | None = None,
        is_vip: bool | None = None,
        in_jail: bool | None = None,
    ) -> None:
        cursor = await self.db.connection.execute(
            """
            SELECT level, gold, experience, is_pk, is_vip, in_jail
            FROM players
            WHERE player_id = ?
            """,
            (player_id,),
        )
        row = await cursor.fetchone()
        if not row:
            return
        await self.db.connection.execute(
            """
            UPDATE players
            SET level = ?, gold = ?, experience = ?, is_pk = ?, is_vip = ?, in_jail = ?
            WHERE player_id = ?
            """,
            (
                level if level is not None else row["level"],
                gold if gold is not None else row["gold"],
                experience if experience is not None else row["experience"],
                int(is_pk) if is_pk is not None else row["is_pk"],
                int(is_vip) if is_vip is not None else row["is_vip"],
                int(in_jail) if in_jail is not None else row["in_jail"],
                player_id,
            ),
        )
        await self.db.connection.commit()

    async def add_inventory_item(self, player_id: int, item: str) -> None:
        await self.db.connection.execute(
            "INSERT INTO inventories (player_id, item) VALUES (?, ?)", (player_id, item)
        )
        await self.db.connection.commit()

    async def remove_inventory_item(self, player_id: int, item: str) -> None:
        await self.db.connection.execute(
            "DELETE FROM inventories WHERE player_id = ? AND item = ?", (player_id, item)
        )
        await self.db.connection.commit()
