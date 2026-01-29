import sys
import os
import pytest
from unittest.mock import MagicMock, AsyncMock, patch

# Add root directory to sys.path to ensure we can import bot
sys.path.insert(0, os.path.abspath("."))

# Mock the database operations to avoid DB connection errors during import or execution
ops_mock = MagicMock()
sys.modules['gardarika.database.operations'] = ops_mock

import bot

@pytest.mark.asyncio
async def test_choose_name_shows_class_descriptions():
    """
    Test that the choose_name handler displays class descriptions
    instead of just a generic message.
    """
    # Setup
    update = MagicMock()
    context = MagicMock()
    context.user_data = {}
    update.message.text = "TestName"

    # We mock reply_html because we expect the improved version to use it.
    # The old version uses reply_text, so we mock that too.
    update.message.reply_text = AsyncMock()
    update.message.reply_html = AsyncMock()

    # Execution
    await bot.choose_name(update, context)

    # Verification
    # We expect one of these to be called.
    # If the code uses reply_text, args[0] is the text.
    # If reply_html, args[0] is text.

    called_mock = update.message.reply_html if update.message.reply_html.called else update.message.reply_text

    # In the current (bad) state, this might be called, but without descriptions.
    # We want to assert that descriptions ARE present.

    assert called_mock.called, "Neither reply_text nor reply_html was called"

    args, kwargs = called_mock.call_args
    text = args[0] if args else kwargs.get('text', '')

    # Check for keywords from descriptions (from gardarika.character.classes)
    # Warrior: "Мастер ближнего боя"
    # Mage: "Мудрец, черпающий силу"
    # Hunter: "Ловкий и незаметный"

    assert "Мастер ближнего боя" in text, "Warrior description not found in message"
    assert "Мудрец, черпающий силу" in text, "Mage description not found in message"
    assert "Ловкий и незаметный" in text, "Hunter description not found in message"

@pytest.mark.asyncio
async def test_choose_class_shows_faction_descriptions():
    """
    Test that the choose_class handler displays faction descriptions.
    """
    # Setup
    update = MagicMock()
    context = MagicMock()
    context.user_data = {}

    query = MagicMock()
    update.callback_query = query
    query.data = "воин" # User chose warrior
    query.answer = AsyncMock()
    query.edit_message_text = AsyncMock()

    # Execution
    await bot.choose_class(update, context)

    # Verification
    assert query.edit_message_text.called

    args, kwargs = query.edit_message_text.call_args
    text = args[0] if args else kwargs.get('text', '')

    # Check for keywords from descriptions (from gardarika.lore.world)
    # Novgorod: "Торговый и ремесленный центр"
    # Kiev: "Сердце русских земель"
    # Forest Tribes: "Сообщество независимых племен"

    assert "Торговый и ремесленный центр" in text, "Novgorod description not found"
    assert "Сердце русских земель" in text, "Kiev description not found"
    assert "Сообщество независимых племен" in text, "Forest Tribes description not found"
