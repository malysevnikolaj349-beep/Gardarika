import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot import profile

@pytest.mark.asyncio
async def test_profile_ux_emojis():
    # Mock update and context
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock message reply
    update.message.reply_html = AsyncMock()

    # Mock database response
    # The key names must match what bot.py expects from the DB dict
    mock_character = {
        'name': 'TestHero',
        'class_name': 'Warrior',
        'faction_name': 'North',
        'level': 5,
        'experience': 1000,
        'health': 150,
        'mana': 30,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 3,
        'endurance': 8,
        'charisma': 2
    }

    with patch('bot.get_character_by_user_id', return_value=mock_character):
        await profile(update, context)

    # Verify the call was made
    update.message.reply_html.assert_called_once()

    # Get the arguments passed to reply_html
    args, _ = update.message.reply_html.call_args
    message_text = args[0]

    # Check for the presence of "Standardized Emoji Design Tokens" or at least the improved ones
    # We expect these to be present after our fix
    expected_emojis = [
        "📜", # Header
        "👤", # Name
        "🛡", # Class (or similar shield)
        "🚩", # Faction
        "📊", # Level
        "❤️", # Health
        "💧", # Mana
        "💎", # Attributes Header
        "💪", # Strength
        "🦉", # Wisdom
        "🎭", # Charisma
    ]

    for emoji in expected_emojis:
        assert emoji in message_text, f"Expected emoji {emoji} not found in profile message"
