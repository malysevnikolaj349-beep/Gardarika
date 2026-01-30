import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# No global sys.path modification here!
# It breaks other tests during collection.

@pytest.fixture
def bot_env():
    """
    Sets up the environment to import 'bot.py' which resides in root
    and depends on root 'gardarika' package, conflicting with 'src/gardarika'.
    """
    # Save original state
    old_path = sys.path[:]

    # We don't save entire sys.modules as it's mutable and huge,
    # but we track what we need to clean up.

    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SRC_DIR = os.path.join(ROOT_DIR, 'src')

    # Modify path: Prefer ROOT, hide SRC
    if SRC_DIR in sys.path:
        sys.path.remove(SRC_DIR)
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    else:
        sys.path.remove(ROOT_DIR)
        sys.path.insert(0, ROOT_DIR)

    # Unload any existing gardarika modules (likely from src)
    # so we can load them from root
    pre_existing_gardarika = [k for k in sys.modules if k.startswith('gardarika')]
    for k in pre_existing_gardarika:
        del sys.modules[k]

    import bot

    yield bot

    # Teardown
    sys.path[:] = old_path

    # Unload root gardarika modules and bot so they don't pollute other tests
    # forcing re-import from src if needed later
    for k in list(sys.modules.keys()):
        if k.startswith('gardarika') or k == 'bot':
            del sys.modules[k]

@pytest.mark.asyncio
async def test_start_handler_async_db(bot_env):
    bot = bot_env

    with patch('bot.add_user_if_not_exists') as mock_db, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        update = MagicMock()
        user = MagicMock()
        user.id = 12345
        user.mention_html.return_value = "User"
        update.effective_user = user
        update.message.reply_html = AsyncMock()

        context = MagicMock()

        await bot.start(update, context)

        mock_to_thread.assert_awaited_with(mock_db, user.id)

@pytest.mark.asyncio
async def test_profile_handler_async_db(bot_env):
    bot = bot_env

    with patch('bot.get_character_by_user_id') as mock_get_char, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        mock_to_thread.return_value = {
            'name': 'TestChar', 'class_name': 'Warrior', 'faction_name': 'Kiev',
            'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
            'strength': 10, 'dexterity': 10, 'wisdom': 10, 'endurance': 10, 'charisma': 10
        }

        update = MagicMock()
        update.effective_user.id = 12345
        update.message.reply_html = AsyncMock()
        context = MagicMock()

        await bot.profile(update, context)

        mock_to_thread.assert_awaited_with(mock_get_char, 12345)

@pytest.mark.asyncio
async def test_choose_faction_handler_async_db(bot_env):
    bot = bot_env

    with patch('bot.create_character') as mock_create_char, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread, \
         patch('bot.Character') as mock_character_class:

        mock_char_instance = MagicMock()
        mock_char_instance.name = "Hero"
        mock_char_instance.character_class.name = "Warrior"
        mock_char_instance.faction = {'name': "Kiev"}
        mock_char_instance.health = 100
        mock_char_instance.mana = 50
        mock_char_instance.attributes = {}
        mock_character_class.return_value = mock_char_instance

        update = MagicMock()
        query = MagicMock()
        query.answer = AsyncMock()
        query.edit_message_text = AsyncMock()
        query.data = 'kiev'
        update.callback_query = query
        update.effective_user.id = 12345

        context = MagicMock()
        context.user_data = {'name': 'Hero', 'class': 'warrior'}

        await bot.choose_faction(update, context)

        found = False
        for call in mock_to_thread.call_args_list:
            args, kwargs = call
            if args and args[0] == mock_create_char:
                found = True
                break

        assert found, "create_character was not called via asyncio.to_thread"

@pytest.mark.asyncio
async def test_create_character_start_async_db(bot_env):
    bot = bot_env

    with patch('bot.get_character_by_user_id') as mock_get_char, \
         patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:

        mock_to_thread.return_value = None

        update = MagicMock()
        update.effective_user.id = 12345
        update.message.reply_text = AsyncMock()

        context = MagicMock()

        await bot.create_character_start(update, context)

        mock_to_thread.assert_awaited_with(mock_get_char, 12345)
