## 2024-05-22 - [HTML Injection in Character Profiles]
**Vulnerability:** Character names were directly interpolated into HTML-formatted strings in `Character.__str__` without escaping.
**Learning:** Telegram bots using `parse_mode='HTML'` are vulnerable to HTML injection if user input is not sanitized. Malicious input can break message formatting or spoof UI elements.
**Prevention:** Always use `html.escape()` for any user-controlled data before inserting it into an HTML-formatted message or string representation.