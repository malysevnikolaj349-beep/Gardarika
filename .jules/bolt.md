## 2024-05-23 - Async/Sync Mixing Anti-pattern
**Learning:** Mixing async libraries (python-telegram-bot) with synchronous database calls (sqlite3) blocks the event loop, degrading performance for all users when one user triggers a DB operation.
**Action:** Always offload blocking I/O to a thread pool using `asyncio.to_thread` when working within an async context, or switch to an async database driver like `aiosqlite`.
