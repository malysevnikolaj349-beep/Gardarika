## 2026-01-30 - [Blocking DB Calls in Async Handlers]
**Learning:** In `python-telegram-bot` (and asyncio in general), calling synchronous database functions (like `sqlite3` operations) directly inside `async def` handlers blocks the entire event loop. This freezes the bot for all users while the query runs.
**Action:** Always wrap synchronous blocking calls in `await asyncio.to_thread(func, *args)`. This offloads the work to a separate thread, keeping the event loop responsive.

## 2026-01-30 - [Hybrid Namespace Testing]
**Learning:** When a project has packages in both root and `src/` with the same name (e.g., `gardarika`), tests can easily load the wrong one depending on `sys.path` order. `conftest.py` might inject `src` globally, breaking tests that need root modules.
**Action:** For tests requiring root modules that are shadowed by `src`, use a fixture to explicitly manipulate `sys.path` and clean `sys.modules` for that specific test context, restoring it afterwards to avoid side effects.
