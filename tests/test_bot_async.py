import sys
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch
import pytest

# Setup path to prioritize root
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# Fixture to handle environment and imports
@pytest.fixture(scope="function")
def bot_env():
    # Remove src from path if it was added by other tests
    SRC = ROOT / "src"
    if str(SRC) in sys.path:
        sys.path.remove(str(SRC))

    # Remove gardarika modules if they were imported from src
    # This ensures we get the root gardarika package
    to_remove = [k for k in sys.modules if k.startswith('gardarika')]
    for k in to_remove:
        del sys.modules[k]

    # Also remove bot if it was imported
    if 'bot' in sys.modules:
        del sys.modules['bot']

    import bot
    return bot


@pytest.mark.asyncio
async def test_start_async_db(bot_env):
    """Test that start handler uses asyncio.to_thread for DB calls."""
    bot = bot_env

    update = MagicMock()
    context = MagicMock()
    user = MagicMock()
    user.id = 12345
    user.mention_html.return_value = "User"
    update.effective_user = user
    update.message.reply_html = AsyncMock()

    with patch.object(bot, 'add_user_if_not_exists') as mock_db, \
            patch('asyncio.to_thread', new_callable=AsyncMock) as mock_th:

        await bot.start(update, context)

        # Expectation: to_thread should be called with (func, *args)
        # Verify call arguments
        mock_th.assert_called_once_with(mock_db, 12345)
        # Verify DB function was NOT called directly
        mock_db.assert_not_called()


@pytest.mark.asyncio
async def test_profile_async_db(bot_env):
    """Test that profile handler uses asyncio.to_thread for DB calls."""
    bot = bot_env

    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()

    # Mock return value for get_character...
    # It returns a dict-like object.
    char_data = {
        'name': 'TestChar', 'class_name': 'Warrior', 'faction_name': 'Kiev',
        'level': 1, 'experience': 0, 'health': 100, 'mana': 50,
        'strength': 10, 'dexterity': 10, 'wisdom': 10,
        'endurance': 10, 'charisma': 10
    }

    with patch.object(bot, 'get_character_by_user_id') as mock_db, \
            patch('asyncio.to_thread', new_callable=AsyncMock) as mock_th:

        # Setup mock_to_thread to return char_data when awaited
        mock_th.return_value = char_data

        await bot.profile(update, context)

        mock_th.assert_called_once_with(mock_db, 12345)
        mock_db.assert_not_called()


@pytest.mark.asyncio
async def test_create_character_start_async_db(bot_env):
    """Test that create_character_start handler uses to_thread."""
    bot = bot_env

    update = MagicMock()
    context = MagicMock()
    update.effective_user.id = 12345
    update.message.reply_text = AsyncMock()

    with patch.object(bot, 'get_character_by_user_id') as mock_db, \
            patch('asyncio.to_thread', new_callable=AsyncMock) as mock_th:

        mock_th.return_value = None  # No character exists

        await bot.create_character_start(update, context)

        mock_th.assert_called_once_with(mock_db, 12345)
        mock_db.assert_not_called()


@pytest.mark.asyncio
async def test_choose_faction_async_db(bot_env):
    """Test that choose_faction handler uses asyncio.to_thread for DB calls."""
    bot = bot_env

    update = MagicMock()
    context = MagicMock()
    query = MagicMock()
    update.callback_query = query
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()

    context.user_data = {
        'name': 'TestName',
        'class': 'воин',  # warrior
        'faction': 'kiev'
    }
    update.effective_user.id = 12345

    mock_player = MagicMock()
    mock_player.name = 'TestName'
    mock_player.character_class.name = 'Warrior'
    mock_player.faction = {'name': 'Kiev'}
    mock_player.attributes = {}
    mock_player.health = 100
    mock_player.mana = 50

    with patch.object(bot, 'create_character') as mock_db, \
            patch('asyncio.to_thread', new_callable=AsyncMock) as mock_th, \
            patch('bot.Character', return_value=mock_player):

        await bot.choose_faction(update, context)

        # verify calling create_character
        # Arguments are complex, check if called
        assert mock_th.called
        args, kwargs = mock_th.call_args
        assert args[0] == mock_db  # The function passed
        # Check user_id
        assert args[1] == 12345
        mock_db.assert_not_called()
