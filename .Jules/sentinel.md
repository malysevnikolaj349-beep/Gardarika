## 2025-05-20 - HTML Injection in Telegram Messages
**Vulnerability:** User input (character name) was directly interpolated into HTML-formatted Telegram messages (`reply_html` and `Character.__str__`).
**Learning:** Telegram's `parse_mode='HTML'` is susceptible to injection just like web HTML. A user could inject tags like `<b>` or `<i>` to spoof messages or break formatting.
**Prevention:** All user-controlled strings must be passed through `html.escape()` before being interpolated into HTML-formatted messages.
