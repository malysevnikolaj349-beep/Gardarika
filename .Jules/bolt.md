## 2024-05-23 - [Blocking SQLite in Async Handlers]
**Learning:** SQLite file operations are blocking by default and will freeze the asyncio event loop if called directly in async functions.
**Action:** Always wrap synchronous DB calls in `bot.py` handlers with `await asyncio.to_thread(...)` to offload them to a separate thread, keeping the bot responsive.
