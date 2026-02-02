## 2024-05-23 - Visual Polish in Text Interfaces
**Learning:** In text-based interfaces like Telegram bots, emojis serve as critical visual anchors. Replacing plain text lists with emoji-bulleted lists (e.g., 🛡 Class, 📊 Level) significantly improves scannability and "delight" without changing the underlying layout or requiring complex UI components.
**Action:** When working on chat bots, always look for opportunities to replace standard bullet points or labels with context-appropriate emojis to improve cognitive processing speed for the user.

## 2026-02-02 - Consistency in Multi-Channel Output
**Learning:** In systems where UI is generated both manually (handlers) and via object methods (`__str__`), inconsistencies in visual tokens (emojis) create a disjointed experience. Syncing them reinforces the visual language.
**Action:** Always cross-reference `__str__` methods when styling command outputs to ensure the "Identity" of the object remains constant across all views.
