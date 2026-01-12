import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import bot


@pytest.mark.asyncio
async def test_profile_formatting():
    """
    Test that the profile command outputs the character profile
    with the expected rich formatting.
    """
    # Mock update and context
    update = MagicMock()
    update.effective_user.id = 12345
    context = MagicMock()

    # Mock the database response
    # Returning a dict that looks like what operations.get_character_by_user_id
    # returns
    mock_character_data = {
        'name': 'TestHero',
        'class_name': 'Воин',
        'faction_name': 'Киевское Княжество',
        'level': 5,
        'experience': 1500,
        'health': 120,
        'mana': 60,
        'strength': 15,
        'dexterity': 12,
        'wisdom': 8,
        'endurance': 14,
        'charisma': 10
    }

    with patch('bot.get_character_by_user_id',
               return_value=mock_character_data):
        # Setup the reply_html mock
        update.message.reply_html = AsyncMock()

        # Call the profile handler
        await bot.profile(update, context)

        # Verify the output
        update.message.reply_html.assert_called_once()
        args, _ = update.message.reply_html.call_args
        message = args[0]

        # Check for new formatting elements (emojis)
        expected_emojis = [
            '📜', '👤', '🛡', '🚩', '📊', '❤️', '💧', '💎',
            '💪', '🦶', '🦉', '🏇', '🎭'
        ]

        for emoji in expected_emojis:
            assert emoji in message, (
                f"Expected emoji {emoji} not found in profile message"
            )
