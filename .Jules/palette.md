## 2024-05-23 - Visual Polish in Text Interfaces
**Learning:** In text-based interfaces like Telegram bots, emojis serve as critical visual anchors. Replacing plain text lists with emoji-bulleted lists (e.g., 🛡 Class, 📊 Level) significantly improves scannability and "delight" without changing the underlying layout or requiring complex UI components.
**Action:** When working on chat bots, always look for opportunities to replace standard bullet points or labels with context-appropriate emojis to improve cognitive processing speed for the user.

## 2024-05-24 - Centralized Formatting for Consistency
**Learning:** In modular applications, different parts of the system (e.g., bot commands vs. model string representations) often need to display the same entity. Centralizing the formatting logic into a dedicated UX module ensures visual consistency and allows for global style updates (like emoji themes) without hunting down multiple formatted strings.
**Action:** Extract formatting logic into reusable helper functions in a `ux` module rather than duplicating f-strings in multiple layers.
