## 2024-05-23 - Sync DB Calls in Async Handlers
**Learning:** The `bot.py` handlers are `async`, but they were making synchronous calls to `gardarika.database.operations`, which blocks the main event loop. This degrades performance significantly under load as one user's DB operation freezes the bot for everyone.
**Action:** Always verify if imported database functions are sync or async. If sync, wrap them in `asyncio.to_thread` when calling from async handlers to maintain responsiveness.
