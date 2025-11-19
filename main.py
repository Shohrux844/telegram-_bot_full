import asyncio
import logging
import os
import sys

from aiogram import Bot, types

from bot.handlers import dp

from utils.env_data import Config as cf


async def main():
    bot = Bot(token=cf.bot.TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    os.makedirs("downloads", exist_ok=True)
    asyncio.run(main())


