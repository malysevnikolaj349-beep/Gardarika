## 2024-05-22 - Blocking DB Calls in Async Handlers
**Learning:** Synchronous database operations (like sqlite3) inside async handlers block the entire event loop, freezing the bot for all users. Using `asyncio.to_thread` is a simple and effective way to offload these calls without refactoring the DB layer to be async.
**Action:** Check for blocking I/O in all async handlers and wrap them with `asyncio.to_thread`.
