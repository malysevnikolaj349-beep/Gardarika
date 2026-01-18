## 2024-05-24 - HTML Injection in Profile Command
**Vulnerability:** User input (character name) was directly interpolated into HTML strings in `bot.py` and `Character.__str__` without sanitization. This allows users to inject HTML tags, potentially breaking message formatting or spoofing UI elements.
**Learning:** Telegram Bot API's `parse_mode='HTML'` requires strict sanitization of all user-controlled data.
**Prevention:** Wrapped all user inputs in `html.escape()` before rendering.
