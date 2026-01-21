# Sentinel Journal

## 2024-05-22 - HTML Injection in Telegram Messages
**Vulnerability:** User-controlled data (character name, class, faction) was interpolated directly into HTML-formatted strings used in `reply_html`.
**Learning:** Telegram bots using `parse_mode='HTML'` are susceptible to HTML injection just like web apps. Even though script execution isn't possible, formatting spoofing (e.g., closing tags and adding fake content) is a risk.
**Prevention:** Always use `html.escape()` for any dynamic data inserted into Telegram HTML messages, or use a builder pattern that handles escaping automatically.
