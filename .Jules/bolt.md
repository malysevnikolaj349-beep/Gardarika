## 2025-05-23 - Blocking Operations in Async Handlers
**Learning:** In a codebase using `asyncio` (like python-telegram-bot), blocking database operations (e.g., standard `sqlite3` calls) freeze the event loop, preventing the application from handling other concurrent requests. This causes significant latency spikes under load.
**Action:** Wrap all blocking I/O operations in `asyncio.to_thread` when calling them from async handlers. This offloads the blocking work to a separate thread, keeping the event loop responsive.
