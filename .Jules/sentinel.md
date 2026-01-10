## 2024-05-23 - Telegram HTML Injection
**Vulnerability:** User input (character name) was rendered directly into HTML-formatted Telegram messages without escaping.
**Learning:** Telegram's `parse_mode='HTML'` is susceptible to injection attacks where users can break formatting or inject unclosed tags, potentially causing API errors or visual spoofing.
**Prevention:** Always use `html.escape()` on any user-controlled string before inserting it into an HTML-formatted message or template.
