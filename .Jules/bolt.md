## 2026-02-01 - [Blocking DB Calls in Async Handlers]
**Learning:** The `bot.py` handlers were making direct synchronous database calls (`gardarika.database.operations`), blocking the asyncio event loop and degrading concurrency.
**Action:** Always wrap blocking I/O operations (like SQLite calls) in `await asyncio.to_thread(...)` when working within `async def` handlers to maintain application responsiveness.
