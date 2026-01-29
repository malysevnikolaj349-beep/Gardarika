## 2026-01-29 - HTML Injection in Telegram Messages
**Vulnerability:** User-controlled input (Character Name) was directly interpolated into HTML-formatted Telegram messages without escaping, allowing HTML injection.
**Learning:** Telegram Bot API's `parse_mode='HTML'` requires manual escaping of all dynamic data using `html.escape()`. Unlike some web frameworks, there is no auto-escaping template engine here.
**Prevention:** Always wrap user input in `html.escape()` before formatting it into a message string intended for `parse_mode='HTML'`.
