from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from app.core.config import settings

router = Router()


@router.message(Command("admin"))
async def handle_admin(message: Message) -> None:
    if message.from_user is None:
        return
    if settings.admin_id_list and message.from_user.id not in settings.admin_id_list:
        await message.answer("Доступ запрещен.")
        return
    webapp_url = f"{settings.base_url}/?token={settings.admin_webapp_token}"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть Панель Бога", web_app=WebAppInfo(url=webapp_url))]
        ]
    )
    await message.answer("Панель управления готова.", reply_markup=keyboard)
