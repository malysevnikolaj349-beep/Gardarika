## 2024-05-23 - Telegram HTML Injection
**Vulnerability:** User input (character name) was injected directly into Telegram HTML messages without escaping.
**Learning:** Telegram `parse_mode='HTML'` requires manual escaping of all user-controlled variables using `html.escape()`, otherwise injection can break formatting or allow spoofing.
**Prevention:** Always wrap variable interpolation in `html.escape()` when constructing HTML messages for Telegram.
