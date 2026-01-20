## 2026-01-20 - Unescaped User Input in HTML Messages
**Vulnerability:** HTML Injection (Stored XSS equivalent) in user profiles. The `profile` command handler and `Character.__str__` method constructed HTML messages using user-controlled data (character name) without escaping it.
**Learning:** Even in restricted environments like Telegram, structured message formats (HTML/Markdown) require input sanitization. Dictionaries returned from database queries are raw data and should not be trusted implicitly.
**Prevention:** Always use `html.escape()` when inserting variable data into HTML strings, especially when using f-strings for formatting. Validate or sanitize data at the entry point (input) or before rendering (output).
