## 2026-01-15 - Asyncio Event Loop Blocking
**Learning:** The project uses `python-telegram-bot` (asyncio) but relies on synchronous `sqlite3` operations in `gardarika.database`. This causes the entire event loop to freeze during DB calls, killing concurrency.
**Action:** Always wrap synchronous DB calls in `bot.py` with `asyncio.to_thread`. Do not rewrite DB layer to async (keep it simple/synchronous as per architecture), just offload it at the call site.

## 2026-01-15 - Split Package Shadowing
**Learning:** The `gardarika` package exists in both root and `src/`. Root contains `bot.py` dependencies (database, character), while `src/` contains `app` and `admin`. Standard `pytest` discovery fails because `src/gardarika` shadows root `gardarika` (or vice versa depending on path order), causing import errors.
**Action:** Run tests for `bot.py` with `PYTHONPATH=$(pwd)` (or relying on implicit CWD). Run tests for `src/` explicitly from `src/` or by setting PYTHONPATH carefully. Do not assume all tests can run in one sweep.
