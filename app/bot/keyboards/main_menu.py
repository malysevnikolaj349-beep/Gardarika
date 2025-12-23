from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from app.core.config import settings

HELP_CALLBACK = "help_menu"
INFO_CALLBACK = "info_menu"


def build_main_keyboard(is_admin: bool) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📜 Команды", callback_data=HELP_CALLBACK),
            InlineKeyboardButton(text="📘 Правила", url=settings.bot_rules_url),
            InlineKeyboardButton(text="💬 Сообщество", url=settings.bot_community_url),
        ]
    ]
    if is_admin:
        webapp_url = f"{settings.base_url}/?token={settings.admin_webapp_token}"
        buttons.append(
            [InlineKeyboardButton(text="👑 Панель Бога", web_app=WebAppInfo(url=webapp_url))]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)
