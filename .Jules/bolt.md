## 2024-05-22 - [Blocking I/O in Async Handlers]
**Learning:** Python's `asyncio` event loop is blocked by synchronous database operations, even if they are fast (like SQLite). In `python-telegram-bot` handlers, this causes the bot to freeze for all users during query execution.
**Action:** Always wrap synchronous blocking calls (like SQLite queries) with `asyncio.to_thread` when calling them from an `async` function. Verified this using `threading.current_thread()` in tests.
