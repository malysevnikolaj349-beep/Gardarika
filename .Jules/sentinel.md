## 2024-05-22 - HTML Injection in Profile Display
**Vulnerability:** User input (character name) was being interpolated directly into HTML-formatted strings used for Telegram messages (`reply_html` and `Character.__str__`).
**Learning:** Even in non-web environments like Telegram bots, `parse_mode='HTML'` makes the application vulnerable to injection attacks. A user could inject tags to break the display or potentially exploit parser behaviors.
**Prevention:** All user-controlled input destined for HTML-formatted output must be sanitized using `html.escape()`. Added explicit escaping in `bot.py` and `Character.__str__`.
