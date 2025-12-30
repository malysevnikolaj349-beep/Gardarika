## 2025-05-23 - HTML Injection in Telegram Bot
**Vulnerability:** The bot displayed user-provided character names directly in `reply_html` messages without escaping, allowing injection of arbitrary HTML tags.
**Learning:** Using `f-strings` with `parse_mode='HTML'` in Telegram bots is vulnerable to injection if user input is not escaped. This is effectively XSS for bots.
**Prevention:** Always use `html.escape()` for user-controlled strings when constructing HTML messages, or use builder functions that handle escaping.
