## 2024-05-23 - Unescaped HTML in Character Profile
**Vulnerability:** User input (character name) was injected directly into HTML strings in `Character.__str__` and `bot.py` profile handler, leading to potential HTML injection.
**Learning:** Even with a restricted HTML parser like Telegram's, it's crucial to escape user input to prevent formatting injection or UI spoofing. The split package structure (`gardarika` in root vs `src/gardarika`) makes running the full test suite difficult.
**Prevention:** Always use `html.escape()` when interpolating user-controlled strings into HTML templates. Ensure comprehensive test coverage for security boundaries.
