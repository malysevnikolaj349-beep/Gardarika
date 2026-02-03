## 2024-10-24 - [Critical] HTML Injection in Character Profile

**Vulnerability:** User-controlled character names were directly interpolated into HTML strings in `bot.py` and `Character.__str__`. This allowed users to inject arbitrary HTML tags (e.g., `<b>`, `<i>`, or even `<a href="...">`) into their profile display.

**Learning:** Telegram's `parse_mode='HTML'` respects certain tags. If user input is not escaped, they can break the message formatting or spoof information. While Telegram sanitizes dangerous scripts, layout spoofing is still a risk.

**Prevention:** Always use `html.escape()` on any user-provided string before inserting it into a message formatted with `parse_mode='HTML'`.
