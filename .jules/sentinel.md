## 2024-05-23 - [HTML Injection in User Profiles]
**Vulnerability:** User input (character name) was being inserted directly into HTML-formatted strings in `bot.py` and `Character.__str__` without escaping. This allowed users to inject HTML tags (e.g., `<b>`, `<a>`) into their profile display.
**Learning:** Even in limited environments like Telegram messages, HTML injection can be used for phishing or spoofing. Always treat user input as untrusted, especially when using formatting modes like `HTML`.
**Prevention:** Use `html.escape()` for all user-controlled data before interpolating it into HTML strings.
