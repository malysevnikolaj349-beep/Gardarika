## 2024-05-22 - HTML Injection in Telegram Messages
**Vulnerability:** User-controlled input (Character Name) was directly inserted into HTML-formatted Telegram messages without sanitization.
**Learning:** Even in "text-only" environments like chat bots, if the platform supports HTML/Markdown parsing (like Telegram's `parse_mode='HTML'`), unescaped input can break formatting (DoS) or allow spoofing (HTML Injection).
**Prevention:** Always use `html.escape()` when inserting dynamic data into HTML-formatted strings for Telegram messages.
