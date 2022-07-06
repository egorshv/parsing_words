import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
from db_dispatcher import DbDispatcher
from states import AddUrl
from parser import get_data
from data_writing import write_data

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
data = DbDispatcher('data.db')
urls = DbDispatcher('urls.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('This is my bot for learning new words')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        '/get_words - выдаёт список слов из бд\n'
        '/add_url - возможность добавить ссылку на документацию\n'
        '/get_urls - выдаёт список введённых ссылок')


@dp.message_handler(commands=['get_words'])
async def get_words(message: types.Message):
    words = [f'{item[1]}: {item[2]}' for item in data.read_all_data('data')]
    if len(words) > 0:
        n = 0
        while n < len(words):
            await message.answer('\n'.join(words[n:n + 100]))
            n += 100
    else:
        await message.answer('Слов пока нет')


@dp.message_handler(commands=['add_url'])
async def add_url(message: types.Message):
    await AddUrl.url.set()
    await message.answer('Введите название и ссылку на документацию через пробел')


@dp.message_handler(state=AddUrl.url)
async def write_url(message: types.Message, state: FSMContext):
    try:
        msg_data = message.text.split()
        urls.write_data({'name': msg_data[0], 'url': msg_data[1]}, 'urls')
        await message.answer('Запись прошла успешно')
        await state.finish()
        all_words = get_data()
        write_data(all_words)
    except Exception as e:
        await message.answer(f'Что-то пошло не так\nОшибка: {e}')


@dp.message_handler(commands=['get_urls'])
async def get_urls(message: types.Message):
    arr = [f'{item[1]}: {item[2]}' for item in urls.read_all_data('urls')]
    if len(arr) > 0:
        await message.answer('\n'.join(arr))
    else:
        await message.answer('Ссылок пока нет')


async def shutdown(dispatcher: Dispatcher):
    data.close_connection()
    urls.close_connection()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
