## 2025-02-17 - HTML Injection in Telegram Bot Profile
**Vulnerability:** The `profile` handler in `bot.py` and `Character.__str__` constructed HTML messages using unescaped user input (character name), allowing HTML injection.
**Learning:** Telegram bot messages using `parse_mode='HTML'` are susceptible to injection. Developers often overlook this when formatting messages manually or in `__str__` methods.
**Prevention:** Always use `html.escape()` when inserting user-controlled data into HTML-formatted strings.
