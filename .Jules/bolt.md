# Bolt's Performance Journal ⚡

## 2026-01-26 - Blocking Database Calls in Async Handlers
**Learning:** SQLite operations are synchronous and block the asyncio event loop when called directly in async handlers (like `python-telegram-bot` handlers). This freezes the entire bot for all users while one disk I/O operation completes.
**Action:** Always wrap blocking I/O calls (like `sqlite3` cursors) in `await asyncio.to_thread(func, *args)` to offload them to a separate thread, keeping the main event loop responsive.
