# Modules

from aiogram import Bot, Dispatcher
import logging
import config
from sqlighter import Sqlighter

# Log

logging.basicConfig(level=logging.INFO)

# Default Var

bot = Bot(config.token)
dp = Dispatcher(bot)
db = Sqlighter("db.db")
