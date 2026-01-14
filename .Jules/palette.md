## 2024-05-23 - Visual Polish in Text Interfaces
**Learning:** In text-based interfaces like Telegram bots, emojis serve as critical visual anchors. Replacing plain text lists with emoji-bulleted lists (e.g., 🛡 Class, 📊 Level) significantly improves scannability and "delight" without changing the underlying layout or requiring complex UI components.
**Action:** When working on chat bots, always look for opportunities to replace standard bullet points or labels with context-appropriate emojis to improve cognitive processing speed for the user.

## 2024-05-24 - Consistency in Multi-View Profiles
**Learning:** When character data is displayed in multiple places (e.g., creation flow vs. profile command), visual inconsistencies (different emojis, formatting) break immersion and trust.
**Action:** Ensure that the "source of truth" for display logic (like `__str__` methods) is used consistently, or if manual formatting is required, it must be rigorously synchronized with the canonical design tokens.
