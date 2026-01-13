import sys
import os

# Force root directory to be first in sys.path to resolve 'gardarika' from root instead of 'src/gardarika'
sys.path.insert(0, os.path.abspath("."))

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bot import start, profile

@pytest.mark.asyncio
async def test_start_handler():
    # Mock Update and Context
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "<a href='tg://user?id=12345'>TestUser</a>"
    update.effective_user = user

    # Mock message reply
    update.message.reply_html = AsyncMock()

    # Mock database operation
    with patch("bot.add_user_if_not_exists") as mock_add_user:
        await start(update, context)

        # Verify DB call
        mock_add_user.assert_called_once_with(12345)

        # Verify reply
        update.message.reply_html.assert_called_once()
        args, _ = update.message.reply_html.call_args
        assert "Привет, <a href='tg://user?id=12345'>TestUser</a>" in args[0]

@pytest.mark.asyncio
async def test_profile_handler_existing_character():
    # Mock Update and Context
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock message reply
    update.message.reply_html = AsyncMock()

    # Mock character data
    character_data = {
        'name': 'Bogatyr',
        'class_name': 'Воин',
        'faction_name': 'Киевское Княжество',
        'level': 1,
        'experience': 0,
        'health': 100,
        'mana': 50,
        'strength': 10,
        'dexterity': 5,
        'wisdom': 3,
        'endurance': 8,
        'charisma': 4
    }

    # Mock database operation
    with patch("bot.get_character_by_user_id", return_value=character_data) as mock_get_char:
        await profile(update, context)

        # Verify DB call
        mock_get_char.assert_called_once_with(12345)

        # Verify reply
        update.message.reply_html.assert_called_once()
        args, _ = update.message.reply_html.call_args
        assert "Bogatyr" in args[0]
        assert "Воин" in args[0]

@pytest.mark.asyncio
async def test_profile_handler_no_character():
    # Mock Update and Context
    update = MagicMock()
    context = MagicMock()

    # Mock user
    user = MagicMock()
    user.id = 12345
    update.effective_user = user

    # Mock message reply
    update.message.reply_text = AsyncMock()

    # Mock database operation
    with patch("bot.get_character_by_user_id", return_value=None) as mock_get_char:
        await profile(update, context)

        # Verify DB call
        mock_get_char.assert_called_once_with(12345)

        # Verify reply
        update.message.reply_text.assert_called_once()
