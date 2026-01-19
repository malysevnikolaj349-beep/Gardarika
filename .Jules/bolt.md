## 2026-01-19 - [Synchronous DB calls in Async Handlers]
**Learning:** The `bot.py` handlers were blocking the asyncio event loop by calling synchronous database operations directly. This stops the bot from responding to other users while a query is running.
**Action:** Use `asyncio.to_thread` to wrap blocking synchronous calls in async handlers to maintain responsiveness.
