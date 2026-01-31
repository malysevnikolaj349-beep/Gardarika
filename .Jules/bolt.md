## 2026-01-31 - [Blocking DB Calls in Async Handlers]
**Learning:** `bot.py` handlers were making synchronous blocking calls to `sqlite3`, freezing the event loop. `asyncio.to_thread` is the clean fix for integrating blocking I/O in async bots without rewriting the DB layer.
**Action:** Always verify if imported database functions are async. If they use blocking drivers (like `sqlite3`), wrap them in `asyncio.to_thread`.
