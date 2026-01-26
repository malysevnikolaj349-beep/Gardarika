## 2026-01-26 - HTML Injection in Telegram Messages
**Vulnerability:** User input (character name) was inserted directly into HTML-formatted messages (`reply_html` and `Character.__str__`) without escaping.
**Learning:** Even in Telegram bots, HTML injection is possible if `ParseMode.HTML` is used. Malicious users could break formatting or insert misleading links.
**Prevention:** Always use `html.escape()` when inserting user-controlled strings into HTML messages, or use `mention_html` for user mentions.
