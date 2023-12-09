from aiogram import F, Bot, Dispatcher, types
from aiogram.enums import ContentType
import asyncio

from datetime import datetime, timedelta
from handlers import start

from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()

dp.include_routers(
    start.router
)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())