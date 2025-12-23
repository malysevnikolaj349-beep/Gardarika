from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Добро пожаловать в Gardarika! Используйте /admin для панели управления (только для богов)."
    )
