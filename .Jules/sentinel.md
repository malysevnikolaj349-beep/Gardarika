## 2024-05-23 - HTML Injection (Telegram XSS)
**Vulnerability:** User input (character name) was rendered directly into HTML-formatted messages without escaping.
**Learning:** Telegram bots using `parse_mode='HTML'` are vulnerable to HTML injection if user input contains valid HTML tags.
**Prevention:** Always use `html.escape()` on user-controlled data before inserting it into HTML strings.
