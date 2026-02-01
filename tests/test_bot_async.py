import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch
import importlib


@pytest.fixture
def mock_update_context():
    update = MagicMock()
    context = MagicMock()
    update.effective_user = MagicMock()
    update.effective_user.id = 12345
    update.effective_user.mention_html.return_value = "TestUser"
    update.message = MagicMock()
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}
    return update, context


@pytest.fixture
def bot_env():
    """
    Sets up the environment to import 'bot.py' which uses the root 'gardarika'.
    Restores the environment afterwards.
    """
    # Save original state
    old_path = list(sys.path)
    old_modules = sys.modules.copy()

    # Path manipulation
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SRC_DIR = os.path.join(ROOT_DIR, 'src')

    # Ensure ROOT is first, SRC is removed
    if SRC_DIR in sys.path:
        sys.path.remove(SRC_DIR)
    if ROOT_DIR not in sys.path:
        sys.path.insert(0, ROOT_DIR)
    else:
        sys.path.remove(ROOT_DIR)
        sys.path.insert(0, ROOT_DIR)

    # Clear gardarika modules to force reload from root
    for module in list(sys.modules.keys()):
        if module.startswith('gardarika'):
            del sys.modules[module]

    import bot
    importlib.reload(bot)

    yield bot

    # Teardown: Restore original state
    sys.path[:] = old_path

    # Restore old modules. First clear any new ones.
    # We want to restore the exact state of sys.modules
    # But we can't easily 'del' everything.
    # However, for 'gardarika', we should definitely reset.
    for module in list(sys.modules.keys()):
        if module.startswith('gardarika') or module == 'bot':
            del sys.modules[module]

    # Put back old modules
    # Note: This doesn't remove NEW modules unrelated to gardarika/bot,
    # but that should be fine.
    # Crucially, we restore gardarika if it was there.
    for k, v in old_modules.items():
        sys.modules[k] = v


@pytest.mark.asyncio
async def test_start_uses_to_thread(mock_update_context, bot_env):
    update, context = mock_update_context
    bot = bot_env

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.add_user_if_not_exists') as mock_db_func:
            await bot.start(update, context)

            # Expectation: to_thread called with the function and user_id
            mock_to_thread.assert_called_with(mock_db_func, 12345)


@pytest.mark.asyncio
async def test_profile_uses_to_thread(mock_update_context, bot_env):
    update, context = mock_update_context
    bot = bot_env

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.get_character_by_user_id') as mock_get_char:
            # Setup return value so logic proceeds if needed
            mock_to_thread.return_value = {
                'name': 'Test',
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
            mock_get_char.return_value = mock_to_thread.return_value

            await bot.profile(update, context)

            mock_to_thread.assert_called_with(mock_get_char, 12345)


@pytest.mark.asyncio
async def test_create_character_start_uses_to_thread(
    mock_update_context, bot_env
):
    update, context = mock_update_context
    bot = bot_env

    with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_to_thread:
        with patch('bot.get_character_by_user_id') as mock_get_char:
            mock_to_thread.return_value = None
            mock_get_char.return_value = None

            await bot.create_character_start(update, context)

            mock_to_thread.assert_called_with(mock_get_char, 12345)


@pytest.mark.asyncio
async def test_choose_faction_uses_to_thread(mock_update_context, bot_env):
    update, context = mock_update_context
    bot = bot_env
    context.user_data = {'name': 'Hero', 'class': 'воин', 'faction': 'kiev'}
    update.effective_user.id = 12345

    with patch('bot.Character') as MockCharacter:
        player_mock = MagicMock()
        player_mock.name = 'Hero'
        player_mock.character_class.name = 'Воин'
        player_mock.faction = {'name': 'Киев'}
        player_mock.health = 100
        player_mock.mana = 50
        player_mock.attributes = {}
        MockCharacter.return_value = player_mock

        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_th:
            with patch('bot.create_character') as mock_create_char:
                await bot.choose_faction(update, context)

                assert mock_th.called
                args, _ = mock_th.call_args
                assert args[0] == mock_create_char
                assert args[1] == 12345
