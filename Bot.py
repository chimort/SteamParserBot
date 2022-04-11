import logging

from os import getenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Choose currency', 'See discounts']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("What's next", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)