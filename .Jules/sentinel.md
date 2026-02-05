## 2025-02-18 - HTML Injection in Telegram Bot Messages
**Vulnerability:** User-controlled input (character name) was interpolated directly into HTML-formatted strings sent to Telegram without escaping.
**Learning:** Telegram's `parse_mode='HTML'` is strict. Unescaped characters like `<` or `&` can cause the Telegram API to reject the entire message, leading to a Denial of Service for that user interaction, in addition to standard spoofing risks.
**Prevention:** Always wrap user-provided strings with `html.escape()` before interpolating them into HTML message templates.
