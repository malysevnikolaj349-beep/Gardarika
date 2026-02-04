## 2024-05-22 - Unsanitized User Input in Telegram HTML Messages
**Vulnerability:** User input (character name) was directly interpolated into f-strings used with `reply_html` and `ParseMode.HTML`.
**Learning:** Telegram bot messages using HTML parse mode are susceptible to injection just like web pages. Developers often assume chat inputs are safe.
**Prevention:** Always use `html.escape()` when inserting variable data into HTML-formatted messages.
