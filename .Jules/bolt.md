## 2024-05-22 - [Blocking Database Operations in Async Handlers]
**Learning:** `bot.py` handlers are async but call synchronous database operations (SQLite) directly. This blocks the asyncio event loop, causing the bot to become unresponsive to other requests while a database query is running.
**Action:** Wrap all blocking database calls in `asyncio.to_thread()` within async handlers to offload them to a separate thread pool, keeping the event loop responsive.
