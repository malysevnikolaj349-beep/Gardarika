## 2024-05-22 - [Blocking DB Calls in Async Handlers]
**Learning:** Python Telegram Bot handlers are async, but standard SQLite calls are synchronous. Using them directly blocks the event loop, freezing the bot for all users.
**Action:** Always wrap synchronous DB operations in `asyncio.to_thread` within async handlers to offload them to a separate thread pool.
