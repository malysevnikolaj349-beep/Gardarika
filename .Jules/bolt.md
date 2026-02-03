## 2024-05-22 - [Backend Performance: Blocking DB Calls]
**Learning:** SQLite operations in `gardarika.database.operations` are synchronous (blocking). Calling them directly in async Telegram handlers (`bot.py`) blocks the main event loop, preventing the bot from handling other updates concurrently.
**Action:** Always wrap blocking I/O calls in `await asyncio.to_thread(...)` when working within `python-telegram-bot` async handlers.
