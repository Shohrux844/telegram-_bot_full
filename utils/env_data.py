from os import getenv
from dotenv import load_dotenv
from utils.settings import BASE_DIR, ENV_PATH

load_dotenv(ENV_PATH)


class BotConfig:
    TOKEN = getenv("BOT_TOKEN")


class DbConfig:
    DB_NAME = getenv("DB_NAME")
    DB_USER = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_URL = getenv("DB_URL")



class Config:
    bot = BotConfig()
    db = DbConfig()