## 2024-05-22 - [Blocking DB Calls in Async Handlers]
**Learning:** `python-telegram-bot` uses `asyncio` for its event loop. Calling blocking functions (like `sqlite3` operations) directly inside async handlers blocks the entire event loop, preventing the bot from processing other updates or tasks until the blocking call returns.
**Action:** Always wrap blocking I/O operations (Database, File I/O) using `await asyncio.to_thread(func, *args)` when working within async handlers to offload execution to a separate thread pool.
