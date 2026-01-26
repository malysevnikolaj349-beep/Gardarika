## 2024-05-24 - HTML Injection in Character Profile
**Vulnerability:** The `Character.__str__` method returned an HTML-formatted string including `self.name` without escaping it. Since `self.name` is user-controlled, this allowed HTML injection (e.g., `<b style="...">`).
**Learning:** In Telegram bots, even if the "frontend" is chat, `parse_mode='HTML'` makes the bot vulnerable to injection attacks if user input is not sanitized.
**Prevention:** Always use `html.escape()` for any user-controlled variable interpolated into an HTML-formatted string.
