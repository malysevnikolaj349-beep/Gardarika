## 2025-02-18 - Synchronous SQLite Blocking Async Handlers
**Learning:** The project uses standard synchronous `sqlite3` calls within asynchronous `python-telegram-bot` handlers. This blocks the main event loop, preventing the bot from processing concurrent updates during database operations.
**Action:** Always wrap `gardarika.database.operations` calls in `await asyncio.to_thread(...)` when calling them from async functions in `bot.py` or other async contexts.
