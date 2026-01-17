## 2024-05-22 - [HTML Injection in Telegram Messages]
**Vulnerability:** User input (specifically character name) was being interpolated directly into HTML-formatted strings in `bot.py` and `Character.__str__` without sanitization. This allowed users to inject HTML tags (e.g., `<b>`, `<i>`), potentially breaking message formatting or spoofing content.
**Learning:** `python-telegram-bot` with `parse_mode='HTML'` does not automatically escape variables in f-strings. Explicit use of `html.escape()` is required for all user-controlled data.
**Prevention:** Always wrap user input in `html.escape()` before including it in HTML-formatted messages. Added `tests/test_security_html_injection.py` as a regression test.
