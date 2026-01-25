## 2026-01-25 - HTML Injection via User Input in Telegram Messages
**Vulnerability:** User-controlled input (character name) is inserted directly into HTML-formatted Telegram messages without escaping, allowing for HTML injection (e.g., `<script>`, `<b>`, `<a>`).
**Learning:** Telegram bot messages using `ParseMode.HTML` treat all interpolated text as HTML code. This allows users to disrupt formatting or potentially mask links if input is not sanitized.
**Prevention:** Use `html.escape()` on all user-provided strings before interpolating them into message templates intended for `ParseMode.HTML`.
