# Bolt's Journal

## 2024-05-23 - Async Database Operations
**Learning:** `python-telegram-bot` uses an asyncio event loop. Calling synchronous database functions directly blocks the loop, causing performance issues.
**Action:** Always wrap blocking synchronous calls (like DB operations) with `asyncio.to_thread` when working in an async environment to maintain responsiveness.
