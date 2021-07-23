import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token = '1216811072:AAETlaFEtXCiHPCebo9sR9BouIONqXih4vE')
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
