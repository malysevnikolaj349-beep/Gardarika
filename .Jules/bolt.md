## 2024-10-25 - [Blocking SQLite in Async Handlers]
**Learning:** The `bot.py` handlers call synchronous SQLite operations directly. In an async `python-telegram-bot` application, this blocks the event loop, freezing the bot for all users during database queries.
**Action:** Wrap synchronous blocking calls (like DB operations) with `asyncio.to_thread` at the call site to offload them to a separate thread pool, keeping the event loop responsive.
