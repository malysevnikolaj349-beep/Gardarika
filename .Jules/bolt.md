## 2026-01-23 - [Async IO Blocking with SQLite]
**Learning:** Synchronous database operations (like `sqlite3`) in async handlers block the entire Telegram bot event loop, causing unresponsiveness for all users during heavy DB load.
**Action:** Always wrap blocking I/O calls (database, file operations) in `asyncio.to_thread()` within `async` functions to keep the event loop free.
