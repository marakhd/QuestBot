from asyncio import run
import logging
from sys import exit as sys_exit

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

from config import settings
from db import close_db, init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


async def main():
    await init_db()
    try:
        from routers import user_router, primary_grade_router, high_grade_router

        router = Router()

        dp.include_routers(
            user_router,
            primary_grade_router,
            high_grade_router,
            router,
        )

        @router.message()
        async def echo(message: Message):
            await message.answer("Пропиши /start")

        await dp.start_polling(bot)
    finally:
        await close_db()


if __name__ == "__main__":
    try:
        run(main())
    except (KeyboardInterrupt, SystemExit):
        sys_exit(0)
