## 2026-01-16 - HTML Injection in Telegram Bot Profile
**Vulnerability:** User input (character name) was rendered directly in HTML-formatted Telegram messages without escaping, allowing HTML injection (XSS).
**Learning:** Telegram's `parse_mode='HTML'` does not automatically escape variables. Even if not a full browser environment, injection can break formatting or enable phishing via `<a>` tags.
**Prevention:** Always use `html.escape()` for any user-controlled data before inserting it into a string intended for `reply_html` or any HTML rendering.
