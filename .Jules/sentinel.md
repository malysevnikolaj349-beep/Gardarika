## 2024-05-23 - HTML Injection in Telegram Messages
**Vulnerability:** User-controlled input (character name, etc.) was being injected directly into `reply_html` calls in `bot.py` and `Character.__str__`. This allowed users to inject HTML tags (HTML Injection/XSS) which could spoof UI or break message formatting.
**Learning:** `reply_html` (and `parse_mode='HTML'`) in `python-telegram-bot` does not automatically escape variables. Telegram treats it as raw HTML.
**Prevention:** Always use `html.escape()` for any dynamic/user-controlled string when constructing messages with `parse_mode='HTML'`.
