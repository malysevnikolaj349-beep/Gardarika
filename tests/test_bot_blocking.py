
import sys
import os
import threading
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# Add root directory to sys.path to allow importing bot.py
sys.path.append(os.getcwd())

import bot

@pytest.mark.asyncio
async def test_start_handler_blocks_event_loop():
    """
    Test that the start handler calls add_user_if_not_exists on the main thread,
    blocking the event loop.
    """
    # Mock update and context
    update = AsyncMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    # We want to capture the thread name where the DB operation runs
    captured_thread_name = None

    def side_effect(*args, **kwargs):
        nonlocal captured_thread_name
        captured_thread_name = threading.current_thread().name

    # Patch the database operation in bot module
    with patch('bot.add_user_if_not_exists', side_effect=side_effect) as mock_db:
        await bot.start(update, context)

        # Verify it was called
        mock_db.assert_called_once()

        # In the optimized code, it should NOT run on MainThread (asyncio.to_thread uses a thread pool)
        assert captured_thread_name != 'MainThread', \
            f"Expected non-blocking call on a worker thread, but got {captured_thread_name}"

@pytest.mark.asyncio
async def test_profile_handler_blocks_event_loop():
    """
    Test that the profile handler calls get_character_by_user_id on the main thread.
    """
    update = AsyncMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    captured_thread_name = None

    def side_effect(*args, **kwargs):
        nonlocal captured_thread_name
        captured_thread_name = threading.current_thread().name
        return {'name': 'Test', 'class_name': 'Warrior', 'faction_name': 'Kiev',
                'level': 1, 'experience': 0, 'health': 100, 'mana': 10,
                'strength': 10, 'dexterity': 10, 'wisdom': 10, 'endurance': 10, 'charisma': 10}

    with patch('bot.get_character_by_user_id', side_effect=side_effect) as mock_db:
        await bot.profile(update, context)

        mock_db.assert_called_once()
        assert captured_thread_name != 'MainThread', \
             f"Expected non-blocking call on a worker thread, but got {captured_thread_name}"
