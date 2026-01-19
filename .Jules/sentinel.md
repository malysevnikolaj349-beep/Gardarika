## 2024-05-22 - HTML Injection in Telegram Bot
**Vulnerability:** `Character.__str__` and `bot.profile` inserted user-controlled names directly into HTML-formatted Telegram messages without escaping, allowing XSS-like injection (e.g., `<script>`, `<b>` spoofing).
**Learning:** Telegram's `parse_mode='HTML'` requires manual escaping of all user input. The project's split `gardarika` package (root vs `src`) complicates testing, as `pytest` collection can prioritize `src` and hide bugs in root modules used by the actual bot.
**Prevention:** Always use `html.escape()` for any dynamic data interpolated into HTML strings. Ensure regression tests explicitly target the deployment environment's package structure (root for bot).
