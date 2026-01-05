## 2024-05-23 - HTML Injection in Telegram Bot
**Vulnerability:** User input (character name) was being interpolated directly into HTML strings used for Telegram messages in `bot.py` and `Character.__str__`.
**Learning:** Telegram's `parse_mode='HTML'` renders HTML tags. If user input contains tags, it can break formatting or potentially be used for phishing/spoofing, even if scripts are not executed.
**Prevention:** Always use `html.escape()` when inserting user input into HTML-formatted strings, especially when using `reply_html` or returning HTML representations of objects.
