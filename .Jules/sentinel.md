## 2024-05-22 - [XSS] Vulnerability in Telegram Bot HTML Parsing
**Vulnerability:** User input (character name) was being interpolated directly into HTML strings used in `reply_html`. This allowed users to inject HTML tags, potentially breaking message formatting (DoS) or spoofing content (Phishing).
**Learning:** `python-telegram-bot`'s `reply_html` does not automatically escape arguments. Any user-controlled data must be explicitly escaped before interpolation.
**Prevention:** Always use `html.escape()` when formatting messages with `parse_mode='HTML'`. Treat all database content as tainted if it originated from user input.
