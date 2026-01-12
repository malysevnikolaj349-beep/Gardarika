## 2024-05-22 - [Optimizing Blocking DB Calls]
**Learning:** Python Telegram Bot handlers are async, but standard sqlite3 calls are synchronous and blocking. Wrapping them in `asyncio.to_thread` prevents the event loop from freezing, ensuring the bot remains responsive to other users.
**Action:** When working with synchronous DB libraries in an async framework, always wrap blocking calls with `asyncio.to_thread`.
