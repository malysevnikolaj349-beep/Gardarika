## 2026-01-25 - Blocking SQLite Calls in Async Handlers
**Learning:** Python's `sqlite3` module performs blocking I/O. When database operations are called directly within `async` functions (such as `python-telegram-bot` handlers), they block the main event loop. This degrades performance significantly as it forces concurrent requests to be processed sequentially.
**Action:** Always identify blocking I/O operations in async code paths and wrap them using `await asyncio.to_thread(...)` to offload execution to a separate thread, keeping the event loop responsive.
