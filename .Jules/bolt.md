## 2026-01-29 - Blocking DB Calls in Async Handlers
**Learning:** Telegram bot handlers are async, but `gardarika.database.operations` use synchronous `sqlite3` calls. Calling them directly in async handlers blocks the asyncio event loop, causing the bot to freeze for all users during database queries.
**Action:** Always wrap synchronous database operations in `await asyncio.to_thread(...)` when calling them from asynchronous functions to offload execution to a separate thread and keep the event loop non-blocking.
