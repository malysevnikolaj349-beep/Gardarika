## 2024-10-23 - HTML Injection in Telegram Messages
**Vulnerability:** User-controlled input (character name) was interpolated directly into HTML-formatted Telegram messages without escaping.
**Learning:** The `python-telegram-bot` library's `reply_html` method and `parse_mode='HTML'` do not automatically escape input. Developers must manually use `html.escape()`.
**Prevention:** Always wrap user input in `html.escape()` when constructing messages with `parse_mode='HTML'`. Use templating engines that auto-escape by default if possible, or create helper functions for safe message construction.
