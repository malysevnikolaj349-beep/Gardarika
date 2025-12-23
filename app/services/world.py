from app.db.database import Database
from app.schemas.admin import WorldEvent, WorldState


class WorldService:
    def __init__(self, db: Database) -> None:
        self.db = db

    async def get_state(self) -> WorldState:
        cursor = await self.db.connection.execute(
            "SELECT time_mode, time_of_day, weather, season FROM world_state WHERE id = 1"
        )
        row = await cursor.fetchone()
        return WorldState(**row)

    async def update_state(
        self,
        time_mode: str | None = None,
        time_of_day: str | None = None,
        weather: str | None = None,
        season: str | None = None,
    ) -> WorldState:
        state = await self.get_state()
        await self.db.connection.execute(
            """
            UPDATE world_state
            SET time_mode = ?, time_of_day = ?, weather = ?, season = ?
            WHERE id = 1
            """,
            (
                time_mode or state.time_mode,
                time_of_day or state.time_of_day,
                weather or state.weather,
                season or state.season,
            ),
        )
        await self.db.connection.commit()
        return await self.get_state()

    async def list_events(self) -> list[WorldEvent]:
        cursor = await self.db.connection.execute("SELECT id, name, status FROM events")
        rows = await cursor.fetchall()
        return [WorldEvent(**row) for row in rows]

    async def trigger_event(self, event_id: int) -> None:
        await self.db.connection.execute(
            "UPDATE events SET status = 'running' WHERE id = ?", (event_id,)
        )
        await self.db.connection.commit()
