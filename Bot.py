import commands

from os import getenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['See discounts', 'Back']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("What's next?", reply_markup=keyboard)


@dp.message_handler(Text(equals='See discounts'))
async def show_discounts(message: types.Message):
    chat_id = message.chat.id
    await message.answer('Wait...')
    await send_data(chat_id=chat_id)


async def send_data(chat_id=''):
    file = commands.main()
    await bot.send_document(chat_id=chat_id, document=open('Games_price_list.csv', 'rb'))
    await os.remove('Games_price_list.csv')


if __name__ == '__main__':
    executor.start_polling(dp)
