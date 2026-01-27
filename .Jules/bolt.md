## 2026-01-27 - [Asyncio Database Wrapper Pattern]
**Learning:** The project uses synchronous SQLite operations in `gardarika.database` which block the main event loop in `bot.py`. `asyncio.to_thread` is the required pattern to unblock the loop while maintaining the synchronous database layer for simplicity and testability.
**Action:** Always wrap `gardarika.database` calls with `await asyncio.to_thread(func, *args)` when calling them from async handlers in `bot.py`.
