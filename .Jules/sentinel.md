## 2024-05-22 - HTML Injection Vulnerability in Telegram Bot

**Vulnerability:** User input (character name) was being directly injected into HTML-formatted strings in `Character.__str__` and `bot.py`'s `profile` command, allowing for HTML injection (e.g., `<b>Bold</b>` or other supported tags) if `parse_mode='HTML'` is used.

**Learning:** Telegram bots using `parse_mode='HTML'` (or `Markdown`) must explicitly escape all user-provided data. Even if Telegram's HTML support is limited, it is best practice to sanitize inputs to prevent broken formatting or spoofing. Also, `edit_message_text` defaults to `None` for `parse_mode`, which can lead to raw HTML tags being displayed to users if the content was prepared for HTML rendering.

**Prevention:** Always use `html.escape()` for any dynamic content inserted into a string intended for `reply_html` or `parse_mode='HTML'`. Ensure that if a method returns HTML-formatted text (like `__str__`), the consumer uses the appropriate `parse_mode`.
