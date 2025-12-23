from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from app.core.config import settings

router = Router()

HERO_IMAGE_URL = "https://placehold.co/900x450/png?text=Gardarika"
HELP_CALLBACK = "help_menu"
INFO_CALLBACK = "info_menu"


def build_main_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📜 Команды", callback_data=HELP_CALLBACK),
            InlineKeyboardButton(text="✨ О мире", callback_data=INFO_CALLBACK),
        ]
    ]
    if is_admin:
        webapp_url = f"{settings.base_url}/?token={settings.admin_webapp_token}"
        buttons.append(
            [InlineKeyboardButton(text="👑 Панель Бога", web_app=WebAppInfo(url=webapp_url))]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
        HERO_IMAGE_URL,
        caption=caption,
        reply_markup=build_main_keyboard(is_admin),
    )


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    await message.answer(
        "📜 Команды Gardarika\n"
        "/start — главное меню\n"
        "/help — список команд\n"
        "Панель богов доступна только администраторам."
    )


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
