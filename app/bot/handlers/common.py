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
LORE_CALLBACK = "lore_menu"
LORE_SECTION_PREFIX = "lore_section:"

LORE_SECTIONS = {
    "history": {
        "title": "История Гардарики",
        "text": (
            "От северных земель до легендарных столиц — Гардарика помнит падение империй "
            "и рождение героев. Хроники ведутся хранителями рода Лады."
        ),
        "image": "https://placehold.co/900x450/png?text=History+of+Gardarika",
    },
    "clans": {
        "title": "Кланы и союзы",
        "text": (
            "Кланы держат границы, охраняют кузницы и спорят за влияние. "
            "Их гербы хранят силу предков и тайные договоры."
        ),
        "image": "https://placehold.co/900x450/png?text=Clans+and+Alliances",
    },
    "magic": {
        "title": "Магия и ритуалы",
        "text": (
            "Сварог подарил миру дыхание магии. Заклинания питаются рунами, "
            "а ритуалы открывают путь к духам."
        ),
        "image": "https://placehold.co/900x450/png?text=Magic+and+Rituals",
    },
    "creatures": {
        "title": "Существа и легенды",
        "text": (
            "В чащах скрываются лешие, а на перевалах слышен зов грифонов. "
            "Каждое существо — часть древнего договора с землёй."
        ),
        "image": "https://placehold.co/900x450/png?text=Creatures+and+Legends",
    },
    "locations": {
        "title": "Локации",
        "text": (
            "От ледяных фьордов до храмов на вершинах — путешествие по Гардарике "
            "открывает новые квесты и тайники."
        ),
        "image": "https://placehold.co/900x450/png?text=World+Locations",
    },
}


def build_main_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📜 Команды", callback_data=HELP_CALLBACK),
            InlineKeyboardButton(text="✨ О мире", callback_data=INFO_CALLBACK),
        ]
    ]
    buttons.append([InlineKeyboardButton(text="📚 Лор", callback_data=LORE_CALLBACK)])
    if is_admin:
        webapp_url = f"{settings.base_url}/?token={settings.admin_webapp_token}"
        buttons.append(
            [InlineKeyboardButton(text="👑 Панель Бога", web_app=WebAppInfo(url=webapp_url))]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_lore_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="📖 История", callback_data=f"{LORE_SECTION_PREFIX}history")],
        [InlineKeyboardButton(text="🛡️ Кланы", callback_data=f"{LORE_SECTION_PREFIX}clans")],
        [InlineKeyboardButton(text="✨ Магия", callback_data=f"{LORE_SECTION_PREFIX}magic")],
        [InlineKeyboardButton(text="🐉 Существа", callback_data=f"{LORE_SECTION_PREFIX}creatures")],
        [InlineKeyboardButton(text="🗺️ Локации", callback_data=f"{LORE_SECTION_PREFIX}locations")],
    ]
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
        "Лор доступен через кнопку 📚 в меню.\n"
        "Панель богов доступна только администраторам."
    )


@router.callback_query(F.data == HELP_CALLBACK)
async def handle_help_callback(query: CallbackQuery) -> None:
    if query.message:
        await query.message.answer(
            "🧭 Быстрые команды:\n"
            "— /start: главное меню\n"
            "— /help: список команд\n"
            "— 📚 Лор: разделы истории, кланов и магии\n"
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


@router.callback_query(F.data == LORE_CALLBACK)
async def handle_lore_callback(query: CallbackQuery) -> None:
    if query.message:
        await query.message.answer(
            "📚 Разделы лора Гардарики. Выбери тему, чтобы получить легенды и описания.",
            reply_markup=build_lore_keyboard(),
        )
    await query.answer()


@router.callback_query(F.data.startswith(LORE_SECTION_PREFIX))
async def handle_lore_section(query: CallbackQuery) -> None:
    section_key = query.data.replace(LORE_SECTION_PREFIX, "")
    section = LORE_SECTIONS.get(section_key)
    if not section:
        await query.answer("Раздел не найден.", show_alert=True)
        return
    if query.message:
        await query.message.answer_photo(
            section["image"],
            caption=f"**{section['title']}**\n{section['text']}",
            parse_mode="Markdown",
        )
    await query.answer()
