class ProductStates(StatesGroup):
    MENU = State()
    SHOW_ALL = State()
    SHOW_FIRST_5 = State()


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
    await message.answer('\n'.join(products))
    await state.finish()


#It's the same story here, but now we only get the first 5 elements of our product
@dp.message_handler(lambda message: message.text == "Show first 5 products", state=ProductStates.MENU)
async def show_first_5_products(message: types.Message, state: FSMContext):
    products = stepik_parser()
    await message.answer('\n'.join(products[:5]))
    await state.finish()
