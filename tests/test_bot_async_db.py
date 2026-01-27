import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Ensure root is in path to import bot
sys.path.insert(0, os.path.abspath("."))

# Attempt to import bot. If it fails due to environment issues, we skip tests.
try:
    import bot
except ImportError:
    bot = None


@pytest.mark.skipif(bot is None, reason="bot module could not be imported")
@pytest.mark.asyncio
async def test_start_uses_to_thread():
    update = MagicMock()
    update.effective_user.id = 123
    update.message.reply_html = AsyncMock()
    context = MagicMock()

    with patch('bot.add_user_if_not_exists') as mock_db_op:
        with patch(
            'asyncio.to_thread', new_callable=AsyncMock
        ) as mock_thread:
            await bot.start(update, context)

            # Assert to_thread was called with the db operation
            if mock_thread.call_count == 0:
                # If to_thread wasn't called, check if db op was called
                # directly
                if mock_db_op.called:
                    pytest.fail(
                        "Database operation was called synchronously, "
                        "expected asyncio.to_thread"
                    )

            mock_thread.assert_called_with(mock_db_op, 123)


@pytest.mark.skipif(bot is None, reason="bot module could not be imported")
@pytest.mark.asyncio
async def test_profile_uses_to_thread():
    update = MagicMock()
    update.effective_user.id = 123
    update.message.reply_html = AsyncMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    with patch('bot.get_character_by_user_id') as mock_db_op:
        with patch(
            'asyncio.to_thread', new_callable=AsyncMock
        ) as mock_thread:
            # Mock return value of to_thread to simulate DB returning a char
            mock_thread.return_value = {
                'name': 'Test', 'class_name': 'Warrior',
                'faction_name': 'Kiev', 'level': 1, 'experience': 0,
                'health': 100, 'mana': 50, 'strength': 10, 'dexterity': 10,
                'wisdom': 10, 'endurance': 10, 'charisma': 10
            }

            await bot.profile(update, context)

            if mock_thread.call_count == 0:
                if mock_db_op.called:
                    pytest.fail(
                        "Database operation was called synchronously, "
                        "expected asyncio.to_thread"
                    )

            mock_thread.assert_called_with(mock_db_op, 123)


@pytest.mark.skipif(bot is None, reason="bot module could not be imported")
@pytest.mark.asyncio
async def test_create_character_start_uses_to_thread():
    update = MagicMock()
    update.effective_user.id = 123
    update.message.reply_text = AsyncMock()
    context = MagicMock()

    with patch('bot.get_character_by_user_id') as mock_db_op:
        with patch(
            'asyncio.to_thread', new_callable=AsyncMock
        ) as mock_thread:
            mock_thread.return_value = None  # No character yet

            await bot.create_character_start(update, context)

            if mock_thread.call_count == 0:
                if mock_db_op.called:
                    pytest.fail(
                        "Database operation was called synchronously, "
                        "expected asyncio.to_thread"
                    )

            mock_thread.assert_called_with(mock_db_op, 123)


@pytest.mark.skipif(bot is None, reason="bot module could not be imported")
@pytest.mark.asyncio
async def test_choose_faction_uses_to_thread():
    update = MagicMock()
    update.effective_user.id = 123
    update.callback_query = MagicMock()
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    update.callback_query.data = 'kiev'

    context = MagicMock()
    context.user_data = {
        'name': 'Hero',
        'class': 'воин',
        'faction': 'kiev'
    }

    with patch('bot.Character') as mock_character_cls:
        mock_instance = MagicMock()
        mock_instance.name = 'Hero'
        mock_instance.character_class.name = 'Warrior'
        mock_instance.faction = {'name': 'Kiev'}
        mock_instance.health = 100
        mock_instance.mana = 50
        mock_instance.attributes = {}
        mock_character_cls.return_value = mock_instance

        with patch('bot.create_character') as mock_db_op:
            with patch(
                'asyncio.to_thread', new_callable=AsyncMock
            ) as m_th:
                await bot.choose_faction(update, context)

                if m_th.call_count == 0:
                    if mock_db_op.called:
                        pytest.fail(
                            "Database operation was called synchronously, "
                            "expected asyncio.to_thread"
                        )

                assert m_th.call_args[0][0] == mock_db_op
