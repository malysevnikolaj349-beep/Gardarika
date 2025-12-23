from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.core.config import settings
from app.bot.keyboards.main_menu import HELP_CALLBACK, INFO_CALLBACK, build_main_keyboard

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    if message.from_user is None:
        return
    is_admin = message.from_user.id in settings.admin_id_list if settings.admin_id_list else False
    caption = (
        "Добро пожаловать в Gardarika!\n"
        "Здесь тебя ждут приключения, кланы и великие битвы.\n"
        "Жми кнопки ниже, чтобы открыть меню и команды."
    )
    if is_admin:
        caption += "\n\n👑 Ты в списке богов — панель управления доступна ниже."
    await message.answer_photo(
        settings.bot_hero_image_url,
        caption=caption,
        reply_markup=build_main_keyboard(is_admin),
    )


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer(
        "📜 Команды Gardarika\n"
        "/start — главное меню\n"
        "/menu — повторить панель\n"
        "/help — список команд\n"
        "Панель богов доступна только администраторам."
    )


@router.message(Command("menu"))
async def handle_menu(message: Message) -> None:
    if message.from_user is None:
        return
    is_admin = message.from_user.id in settings.admin_id_list if settings.admin_id_list else False
    await message.answer("Главное меню:", reply_markup=build_main_keyboard(is_admin))


@router.callback_query(F.data == HELP_CALLBACK)
async def handle_help_callback(query: CallbackQuery) -> None:
    if query.message:
        await query.message.answer(
            "🧭 Быстрые команды:\n"
            "— /start: главное меню\n"
            "— /help: список команд\n"
            "Для админов доступна панель управления через кнопку 👑."
        )
    await query.answer()


@router.callback_query(F.data == INFO_CALLBACK)
async def handle_info_callback(query: CallbackQuery) -> None:
    if query.message:
        await query.message.answer(
            "✨ Gardarika — это мир эпических клановых войн и легендарных героев.\n"
            "Следи за новостями в чате клана и готовься к новым ивентам!"
        )
    await query.answer()
