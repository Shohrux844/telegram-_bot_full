from aiogram import Dispatcher
from os import getenv

from utils.env_data import Config as cf

TOKEN = cf.bot.TOKEN

dp = Dispatcher()
