import asyncio
import logging
import os

from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = os.getenv('TELEGRAM_BOT')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
    

if __name__ == '__main__':
    executor.start_polling(dp)
