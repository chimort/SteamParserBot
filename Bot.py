import commands
import requests.exceptions

from os import getenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiofiles import os

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher(bot)

game_genre = ''

genres = ['action', 'for one player', 'strategy',
          'horror', 'coop', 'puzzle', 'all']


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = genres
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Which game genre do you want to see?", reply_markup=keyboard)


@dp.message_handler(Text(equals=['action', 'for one player', 'strategy',
                                 'horror', 'coop', 'puzzle', 'all']))
async def genre(message: types.Message):
    s_disc = types.InlineKeyboardButton(text='Continue', callback_data='s_disc')
    change_g = types.InlineKeyboardButton(text='Change genre', callback_data='return')
    inl_k = types.InlineKeyboardMarkup(row_width=2)
    inl_k.insert(change_g)
    inl_k.insert(s_disc)
    global game_genre
    game_genre = message.text
    global msg1
    global msg2
    global chat_id
    chat_id = message.chat.id
    msg1 = await message.answer(f'You choose genre - "{message.text}"', reply_markup=types.ReplyKeyboardRemove())
    msg2 = await message.answer(f'You can Change genre or you can Continue', reply_markup=inl_k)


@dp.callback_query_handler(lambda c: c.data == 'return')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*genres)
    await msg1.delete()
    await msg2.delete()
    await bot.send_message(callback_query.from_user.id,
                           "Which game genre do you want to see?", reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 's_disc')
async def process_callback_button1(callback_query: types.CallbackQuery):
    buttons = ['1-10 games', '1-20 games', 'all games']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await msg1.delete()
    await msg2.delete()
    await bot.send_message(chat_id, text='How many games do you want to see?', reply_markup=keyboard)


@dp.message_handler(Text(equals=['1-10 games', '1-20 games', 'all games']))
async def send_discount(message: types.Message):
    try:
        if message.text == '1-10 games':
            await message.answer('Wait...')
            commands.main(10, genre=game_genre)
            await message.answer(commands.send_not_all_games(10))
            await os.remove('Games.csv')
            await message.answer('/start :-)', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == '1-20 games':
            await message.answer('Wait...')
            commands.main(20, genre=game_genre)
            await message.answer(commands.send_not_all_games(20))
            await os.remove('Games.csv')
            await message.answer('/start :-)', reply_markup=types.ReplyKeyboardRemove())
        else:
            try:
                await message.answer('Wait...')
                await send_all_data(chat_id=chat_id)
            except NameError:
                await message.answer('first you have to write "/start"')
    except requests.exceptions.MissingSchema:
        await message.answer('first you have to write "/start"')


async def send_all_data(chat_id=''):
    file = commands.main(amount=0)
    await bot.send_document(chat_id=chat_id, document=open('Games.csv', 'rb'))
    await os.remove('Games.csv')
    game_genre = ''


if __name__ == '__main__':
    executor.start_polling(dp)
