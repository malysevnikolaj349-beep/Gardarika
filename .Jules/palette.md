## 2024-05-23 - Visual Polish in Text Interfaces
**Learning:** In text-based interfaces like Telegram bots, emojis serve as critical visual anchors. Replacing plain text lists with emoji-bulleted lists (e.g., 🛡 Class, 📊 Level) significantly improves scannability and "delight" without changing the underlying layout or requiring complex UI components.
**Action:** When working on chat bots, always look for opportunities to replace standard bullet points or labels with context-appropriate emojis to improve cognitive processing speed for the user.

## 2024-05-24 - Consistent Formatting across Access Patterns
**Learning:** When domain objects (like Character) have a rich `__str__` representation but the application layer (Bot) accesses raw data (DB rows) for performance or convenience, the visual presentation often diverges, leading to inconsistent UX.
**Action:** Centralize formatting logic in a static method or helper that can accept either the Object or a Dictionary, ensuring a consistent "Visual Voice" regardless of the data source.
