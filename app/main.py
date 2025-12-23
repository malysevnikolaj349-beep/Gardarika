import asyncio
import logging

from aiogram import Bot

from app.bot import create_dispatcher
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import Database
from app.db.migrations import run_migrations, seed_defaults
from app.web.app import start_web_app


async def main() -> None:
    setup_logging()
    if not settings.bot_token:
        logging.warning("BOT_TOKEN is not set. Bot will not start polling.")

    db = Database(settings.database_path)
    await db.connect()
    await run_migrations(db)
    await seed_defaults(db)

    await start_web_app(db)

    if settings.bot_token:
        bot = Bot(token=settings.bot_token)
        dispatcher = create_dispatcher()
        await dispatcher.start_polling(bot)
    else:
        while True:
            await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
