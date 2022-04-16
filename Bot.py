import commands
import requests.exceptions

from os import getenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher(bot)


game_genre = ''


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['action', 'for one player', 'strategy',
                     'horror', 'coop', 'puzzle', 'all']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Which game genre do you want to see?", reply_markup=keyboard)


@dp.message_handler(Text(equals=['action', 'for one player', 'strategy',
                                 'horror', 'coop', 'puzzle', 'all']))
async def genre(message: types.Message):
    genre_buttons = 'See discounts'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(genre_buttons)
    global game_genre
    game_genre = message.text
    await message.answer(f'You choose genre - "{message.text}"', reply_markup=keyboard)


@dp.message_handler(Text(equals='See discounts'))
async def amount_of_discounts(message: types.Message):
    buttons = ['1-10 games', '1-20 games', 'all games']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer('How many games do you want to see?', reply_markup=keyboard)


@dp.message_handler(Text(equals=['1-10 games', '1-20 games', 'all games']))
async def send_discount(message: types.Message):
    chat_id = message.chat.id
    try:
        if message.text == '1-10 games':
            await message.answer('Wait...')
            commands.main(10, genre=game_genre)
            await message.answer(commands.send_not_all_games(10))
            await os.remove('Games.csv')
        elif message.text == '1-20 games':
            await message.answer('Wait...')
            commands.main(20, genre=game_genre)
            await message.answer(commands.send_not_all_games(20))
            await os.remove('Games.csv')
        else:
            await message.answer('Wait...')
            await send_all_data(chat_id)
    except requests.exceptions.MissingSchema:
        await message.answer('first you have to write "/start"')


async def send_all_data(chat_id=''):
    file = commands.main(amount=0)
    await bot.send_document(chat_id=chat_id, document=open('Games.csv', 'rb'))
    await os.remove('Games.csv')


if __name__ == '__main__':
    executor.start_polling(dp)
