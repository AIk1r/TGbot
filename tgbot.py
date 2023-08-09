import asyncio
import logging
import os
import re
import requests

from aiogram import Bot, types, Dispatcher, executor
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = os.getenv('TELEGRAM_BOT')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def func_parser():
    url = "Any site you have with html, not js"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #This is where I use regex to find the information I need.
    #I start by specifying the tag with the first argument and the second argument with the necessary data where to look for the information I need.
    products = soup.find_all('a', {'href': re.compile(r"^/?smth/.*")})

    return products

#This is the command itself for the bot, which will output the information we need when we enter it.
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    products = func_parser()
    course_titles = [product.text.strip() for product in products]
    await message.answer(course_titles) #The output is implemented as a list
    

if __name__ == '__main__':
    executor.start_polling(dp)
