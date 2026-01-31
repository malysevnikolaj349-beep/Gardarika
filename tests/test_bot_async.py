import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

# ENVIRONMENT FIXING ---------------------------------------------------------
# We need to load 'gardarika' from the ROOT directory (where database/ exists),
# not from src/ (where game_engine/ exists).
# conftest.py puts src/ at the front of sys.path. We must override this.

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. Ensure root_dir is at the very front of sys.path
if root_dir in sys.path:
    sys.path.remove(root_dir)
sys.path.insert(0, root_dir)

# 2. Unload 'gardarika' if it was already loaded from src/
if 'gardarika' in sys.modules:
    if 'src' in str(sys.modules['gardarika'].__file__):
        del sys.modules['gardarika']
        # Unload all submodules
        for k in list(sys.modules.keys()):
            if k.startswith('gardarika'):
                del sys.modules[k]

# 3. Import what we need
try:
    import gardarika.database  # noqa: F401
except ImportError as e:
    # If this fails, print debug info
    print(f"DEBUG: sys.path: {sys.path}")
    print(f"DEBUG: root_dir: {root_dir}")
    raise e

import bot  # noqa: E402
# ----------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_start_handler_async_db():
    # Mock the DB function within bot module
    with patch('bot.add_user_if_not_exists'):
        # Mock asyncio.to_thread to verify it's used
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_th:
            update = MagicMock()
            update.effective_user.id = 123
            update.effective_user.mention_html.return_value = "User"
            update.message.reply_html = AsyncMock()

            context = MagicMock()

            await bot.start(update, context)

            # This should fail if optimization is not applied
            mock_to_th.assert_called_with(bot.add_user_if_not_exists, 123)


@pytest.mark.asyncio
async def test_profile_handler_async_db():
    with patch('bot.get_character_by_user_id'):
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_th:
            # Setup mock return for to_thread (simulating db result)
            mock_to_th.return_value = {
                'name': 'TestChar',
                'class_name': 'Warrior',
                'faction_name': 'Kiev',
                'level': 1,
                'experience': 0,
                'health': 100,
                'mana': 50,
                'strength': 10,
                'dexterity': 10,
                'wisdom': 10,
                'endurance': 10,
                'charisma': 10
            }

            update = MagicMock()
            update.effective_user.id = 123
            update.message.reply_html = AsyncMock()

            context = MagicMock()

            await bot.profile(update, context)

            mock_to_th.assert_called_with(bot.get_character_by_user_id, 123)


@pytest.mark.asyncio
async def test_create_character_start_handler_async_db():
    with patch('bot.get_character_by_user_id'):
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_th:
            mock_to_th.return_value = None  # No character exists

            update = MagicMock()
            update.effective_user.id = 123
            update.message.reply_text = AsyncMock()

            context = MagicMock()

            await bot.create_character_start(update, context)

            mock_to_th.assert_called_with(bot.get_character_by_user_id, 123)
