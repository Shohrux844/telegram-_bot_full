import asyncio
import logging
import sys

from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from bot.handlers import dp

from utils.env_data import Config as cf


async def main():
    bot = Bot(token=cf.bot.TOKEN, default=DefaultBotProperties(parse_mode=types.ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
