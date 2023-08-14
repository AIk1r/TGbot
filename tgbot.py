import asyncio
import logging
import os
import requests

from aiogram import Bot, types, Dispatcher, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
BOT_TOKEN = os.getenv('TELEGRAM_BOT')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


class ProductStates(StatesGroup):
    MENU = State()
    SHOW_ALL = State()
    SHOW_FIRST_5 = State()


#I've redesigned the parser itself, I'm using selenium to get JS data and further work with HTML.
def stepik_parser():
    url = "https://stepik.org/catalog"

    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        #Also removed the regex and did a simple tag and class search, because now I can get the data normally.
        products = soup.find_all('a', class_='course-card__title')
        course_title = [product.text.strip() for product in products]
        return course_title
    finally:
        browser.quit()


#This is the command itself for the bot, which will output the information we need when we enter it.
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    #Right now, the output buttons only work via a call to the '/start' command.
    #That is, you will need to enter the command again to get the information again in some form
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(types.KeyboardButton("Show all products"), types.KeyboardButton("Show first 5 products"))
    await message.answer("Hello! Please select one of the options:", reply_markup=kb)
    await ProductStates.MENU.set()


#When entering the command '/start' we will have two buttons, respectively
#here we select the function to show all products and see all these products
@dp.message_handler(lambda message: message.text == "Show all products", state=ProductStates.MENU)
async def show_all_products(message: types.Message, state: FSMContext):
    products = stepik_parser()
    course_titles = [product.text.strip() for product in products]
    await message.answer(' '.join(course_titles))
    await state.finish()


#It's the same story here, but now we only get the first 5 elements of our product
@dp.message_handler(lambda message: message.text == "Show first 5 products", state=ProductStates.MENU)
async def show_first_5_products(message: types.Message, state: FSMContext):
    products = stepik_parser()
    course_titles = [product.text.strip() for product in products[:5]]
    await message.answer(' '.join(course_titles))
    await state.finish()
    

if __name__ == '__main__':
    executor.start_polling(dp)
