## 2024-10-24 - Blocking SQLite Calls in Async Handlers
**Learning:** SQLite operations are synchronous and block the asyncio event loop in `python-telegram-bot` handlers. Even small queries can degrade performance under load by freezing the bot.
**Action:** Always wrap blocking DB calls in `await asyncio.to_thread(...)` within async handlers to keep the event loop responsive.
