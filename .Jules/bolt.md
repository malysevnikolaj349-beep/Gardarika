## 2024-05-23 - Async Event Loop Blocking
**Learning:** Synchronous database calls (like `sqlite3`) in async Telegram bot handlers block the entire event loop. This means one user's DB query freezes the bot for everyone else.
**Action:** Always wrap blocking I/O calls in `asyncio.to_thread` when working with synchronous drivers in an async environment like `python-telegram-bot`.
