import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = os.getenv('TELEGRAM_BOT')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
    

if __name__ == '__main__':
    executor.start_polling(dp)
