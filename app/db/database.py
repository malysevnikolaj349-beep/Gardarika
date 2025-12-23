import aiosqlite


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        self._connection: aiosqlite.Connection | None = None

    async def connect(self) -> None:
        self._connection = await aiosqlite.connect(self.path)
        self._connection.row_factory = aiosqlite.Row

    async def close(self) -> None:
        if self._connection:
            await self._connection.close()

    @property
    def connection(self) -> aiosqlite.Connection:
        if not self._connection:
            raise RuntimeError("Database connection is not initialized")
        return self._connection
