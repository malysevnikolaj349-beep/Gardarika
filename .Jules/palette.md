## 2024-05-23 - Visual Polish in Text Interfaces
**Learning:** In text-based interfaces like Telegram bots, emojis serve as critical visual anchors. Replacing plain text lists with emoji-bulleted lists (e.g., 🛡 Class, 📊 Level) significantly improves scannability and "delight" without changing the underlying layout or requiring complex UI components.
**Action:** When working on chat bots, always look for opportunities to replace standard bullet points or labels with context-appropriate emojis to improve cognitive processing speed for the user.

## 2024-05-23 - Visual Consistency and Safety
**Learning:** In Telegram bots, consistent emoji usage across different handlers (Profile vs Creation) establishes a stronger visual language. Crucially, all user-generated content (names) must be HTML-escaped even in internal  methods to prevent XSS when these methods are used for display.
**Action:** Audit all string representations of domain models to ensure they use the standard design tokens and sanitize inputs.

## 2024-05-23 - Visual Consistency and Safety
**Learning:** In Telegram bots, consistent emoji usage across different handlers (Profile vs Creation) establishes a stronger visual language. Crucially, all user-generated content (names) must be HTML-escaped even in internal `__str__` methods to prevent XSS when these methods are used for display.
**Action:** Audit all string representations of domain models to ensure they use the standard design tokens and sanitize inputs.
