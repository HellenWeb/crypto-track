# Modules

from aiogram import Bot, Dispatcher
import logging
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlighter import Sqlighter

# Log

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

# Default Var

bot = Bot(config.token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Sqlighter("db.db")
