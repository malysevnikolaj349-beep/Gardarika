# Sentinel Journal

## 2024-05-22 - Telegram HTML Injection
**Vulnerability:** User-controlled input (character name) was interpolated directly into HTML-formatted Telegram messages without escaping. This allows users to inject HTML tags (e.g., `<b>`, `<i>`, or worse) to disrupt formatting or potentially spoof system messages.
**Learning:** `python-telegram-bot` with `parse_mode='HTML'` does not auto-escape input. Developers must manually escape all dynamic content using `html.escape()`. This is a common pattern in this codebase where `f-strings` are used for message construction.
**Prevention:** Always wrap user variables in `html.escape()` when constructing messages with `parse_mode='HTML'`. Added `tests/test_security_html_injection.py` to enforce this for character profiles.
