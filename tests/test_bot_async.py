import sys
import os
import pytest
from unittest.mock import MagicMock, patch, AsyncMock

# --- Environment Setup for Bot Testing ---
# We need to ensure we are testing the root 'gardarika' package.
# This must be done before importing 'bot'.

# 1. Get paths
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
SRC_DIR = os.path.join(ROOT_DIR, 'src')

# 2. Fix sys.path: Remove src, ensure root is present
if SRC_DIR in sys.path:
    sys.path.remove(SRC_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# 3. Clean sys.modules of any 'gardarika' loaded from src
# This is critical because conftest.py might have already triggered an import
modules_to_remove = [m for m in sys.modules if m.startswith('gardarika')]
for m in modules_to_remove:
    if 'src' in getattr(sys.modules[m], '__file__', ''):
        del sys.modules[m]

# Now we can import bot and it should use root/gardarika
import bot  # noqa: E402


# --- Tests ---


@pytest.mark.asyncio
async def test_start_handler_offloads_to_thread():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    # We patch asyncio.to_thread AND the db operation
    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        # We need to verify it's called with the specific function
        # But wait, bot.py imports add_user_if_not_exists directly.
        # So we should check if to_thread was called with that function object.

        # However, bot.py does:
        # from gardarika.database.operations import add_user_if_not_exists
        # So we need to access it via bot.add_user_if_not_exists
        # for comparison, or patch it in bot module.

        with patch('bot.add_user_if_not_exists') as mock_db_func:
            await bot.start(update, context)

            # Verify to_thread was called
            assert mock_to_thread.called
            # Verify the first arg to to_thread was our db function
            args, _ = mock_to_thread.call_args
            assert args[0] == mock_db_func
            # Verify the args passed to the db function
            assert args[1] == 12345


@pytest.mark.asyncio
async def test_profile_handler_offloads_to_thread():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        # Mock the return value of the DB call to be None
        mock_to_thread.return_value = None

        with patch('bot.get_character_by_user_id') as mock_db_func:
            await bot.profile(update, context)

            assert mock_to_thread.called
            args, _ = mock_to_thread.call_args
            assert args[0] == mock_db_func
            assert args[1] == 12345


@pytest.mark.asyncio
async def test_create_character_start_offloads_to_thread():
    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    update.effective_user = user
    update.message.reply_text = AsyncMock()

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        mock_to_thread.return_value = None  # No character exists

        with patch('bot.get_character_by_user_id') as mock_db_func:
            await bot.create_character_start(update, context)

            assert mock_to_thread.called
            args, _ = mock_to_thread.call_args
            assert args[0] == mock_db_func
            assert args[1] == 12345


@pytest.mark.asyncio
async def test_choose_faction_offloads_to_thread():
    update = MagicMock()
    context = MagicMock()
    query = MagicMock()
    update.callback_query = query
    update.effective_user.id = 12345
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()
    query.data = "kiev"

    # Setup context.user_data
    context.user_data = {
        'name': 'BraveHero',
        'class': 'воин',
        'faction': 'kiev'
    }

    # We need to mock Character creation because it might use logic
    # we don't want to test here.
    # bot.py instantiates Character(name, class, faction).

    mock_char_instance = MagicMock()
    mock_char_instance.name = 'BraveHero'
    mock_char_instance.character_class.name = 'Воин'
    mock_char_instance.faction = {'name': 'Киев'}
    mock_char_instance.health = 100
    mock_char_instance.mana = 50
    mock_char_instance.attributes = {}

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.create_character') as mock_db_func:
            with patch('bot.Character', return_value=mock_char_instance):
                await bot.choose_faction(update, context)

                assert mock_to_thread.called
                args, _ = mock_to_thread.call_args
                assert args[0] == mock_db_func
                # Verify args passed to create_character
                # user_id, name, class, faction, stats
                assert args[1] == 12345
                assert args[2] == 'BraveHero'
