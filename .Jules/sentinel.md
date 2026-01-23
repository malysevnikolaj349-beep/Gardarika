## 2026-01-23 - HTML Injection in Telegram Messages
**Vulnerability:** User input (Character Name) was directly interpolated into HTML strings used by `python-telegram-bot`'s `reply_html` and `ParseMode.HTML`. This allowed users to inject HTML tags (e.g., `<b>`, `<a>`) potentially disrupting UI or creating phishing links.
**Learning:** `python-telegram-bot` does not automatically escape variables in f-strings when using `reply_html`. Developers must manually escape all user-controlled data.
**Prevention:** Always use `html.escape()` on user input before inserting it into HTML-formatted messages. Use a helper function or wrapper if possible to enforce this.
