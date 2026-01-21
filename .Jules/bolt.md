# Bolt's Journal ⚡

This journal tracks critical performance learnings, anti-patterns, and architectural decisions.

## 2024-05-23 - Async Database Wrappers
**Learning:** Blocking synchronous calls (like `sqlite3` operations) in `async` handlers freeze the entire event loop, destroying concurrency.
**Action:** Always wrap blocking calls with `await asyncio.to_thread(...)` at the call site in `bot.py` handlers. Do not make the DB layer async itself to preserve simplicity and testability.
