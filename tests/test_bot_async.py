import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import importlib

@pytest.fixture
def bot_env():
    # Setup: prioritize root
    original_path = sys.path[:]
    original_modules = sys.modules.copy()

    root_dir = os.getcwd()
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    elif sys.path[0] != root_dir:
        sys.path.insert(0, root_dir)

    # Ensure gardarika is loaded from root
    # We must unload 'gardarika' if it's currently from src
    if 'gardarika' in sys.modules:
        if 'src' in getattr(sys.modules['gardarika'], '__file__', ''):
            del sys.modules['gardarika']
            # Remove submodules too
            to_remove = [m for m in sys.modules if m.startswith('gardarika.')]
            for m in to_remove:
                del sys.modules[m]

    try:
        import bot
        # Reload to be sure we got the right one and fresh imports
        importlib.reload(bot)
        yield bot
    finally:
        # Teardown: Restore environment
        sys.path[:] = original_path
        # Restore modules?
        # Restoring sys.modules is tricky because we might have loaded new things.
        # But we should at least remove the 'bot' and 'gardarika' (root version) so other tests don't see them.
        if 'bot' in sys.modules:
            del sys.modules['bot']

        # We should define what "restore" means.
        # If other tests expect 'gardarika' from src, we should probably clear 'gardarika' from modules
        # so they can import their version fresh.
        if 'gardarika' in sys.modules:
             del sys.modules['gardarika']
        to_remove = [m for m in sys.modules if m.startswith('gardarika.')]
        for m in to_remove:
            del sys.modules[m]

        # We can't easily restore the exact state of sys.modules from 'original_modules'
        # because other modules might have been imported correctly.
        # But cleaning up our mess is usually enough.

@pytest.fixture
def mock_update_context():
    update = MagicMock()
    context = MagicMock()
    update.effective_user = MagicMock()
    update.effective_user.id = 12345
    update.effective_user.mention_html.return_value = "<a href='...'>User</a>"
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}
    return update, context

@pytest.mark.asyncio
async def test_start_handler_async_db(bot_env, mock_update_context):
    bot = bot_env
    update, context = mock_update_context

    # We use context managers for patching to ensure they apply to the 'bot' module we just imported
    with patch.object(bot, 'add_user_if_not_exists') as mock_db_call:
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            await bot.start(update, context)
            mock_to_thread.assert_called_with(bot.add_user_if_not_exists, 12345)

@pytest.mark.asyncio
async def test_profile_handler_async_db(bot_env, mock_update_context):
    bot = bot_env
    update, context = mock_update_context

    mock_char = {'name': 'TestChar', 'class_name': 'Warrior', 'faction_name': 'Kiev',
                 'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
                 'strength': 10, 'dexterity': 10, 'wisdom': 10, 'endurance': 10, 'charisma': 10}

    with patch.object(bot, 'get_character_by_user_id', return_value=mock_char):
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            mock_to_thread.return_value = mock_char
            await bot.profile(update, context)
            mock_to_thread.assert_called_with(bot.get_character_by_user_id, 12345)

@pytest.mark.asyncio
async def test_create_character_start_async_db(bot_env, mock_update_context):
    bot = bot_env
    update, context = mock_update_context

    with patch.object(bot, 'get_character_by_user_id', return_value=None):
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
            mock_to_thread.return_value = None
            await bot.create_character_start(update, context)
            mock_to_thread.assert_called_with(bot.get_character_by_user_id, 12345)

@pytest.mark.asyncio
async def test_choose_faction_async_db(bot_env, mock_update_context):
    bot = bot_env
    update, context = mock_update_context
    context.user_data = {'name': 'Hero', 'class': 'воин', 'faction': 'kiev'}

    with patch.object(bot, 'Character') as MockCharacter:
        char_instance = MagicMock()
        char_instance.health = 100
        char_instance.mana = 50
        char_instance.attributes = {}
        char_instance.name = 'Hero'
        char_instance.character_class.name = 'Воин'
        char_instance.faction = {'name': 'Киев'}
        MockCharacter.return_value = char_instance

        with patch.object(bot, 'create_character') as mock_create:
            with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
                await bot.choose_faction(update, context)

                assert mock_to_thread.call_count >= 1
                args, _ = mock_to_thread.call_args
                assert args[0] == bot.create_character
