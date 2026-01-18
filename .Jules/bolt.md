## 2024-05-22 - [Blocking SQLite in Async Handlers]
**Learning:** SQLite operations are synchronous and block the asyncio event loop in `python-telegram-bot` handlers. This causes the bot to become unresponsive to other users during database queries.
**Action:** Wrap all blocking database calls in `asyncio.to_thread` at the call site (in the handler). Do not make the DB functions themselves async to preserve synchronous testability and simplicity of the DB layer.
