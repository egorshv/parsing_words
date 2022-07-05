import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN
from db_dispatcher import DbDispatcher
from states import AddUrl

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
    await message.answer('\n'.join(words))


@dp.message_handler(commands=['add_url'])
async def add_url(message: types.Message):
    await AddUrl.url.set()
    await message.answer('Введите ссылку на документацию')


@dp.message_handler(state=AddUrl.url)
async def write_url(message: types.Message):
    try:
        urls.write_data({'name': 'test', 'url': message.text}, 'urls')
        await message.answer('Запись прошла успешно')
    except Exception as e:
        await message.answer(f'Что-то пошло не так\nОшибка: {e}')


@dp.message_handler(commands=['get_urls'])
async def get_urls(message: types.Message):
    arr = [f'{item[1]}: {item[2]}' for item in urls.read_all_data('urls')]
    await message.answer('\n'.join(arr))


async def shutdown(dispatcher: Dispatcher):
    data.close_connection()
    urls.close_connection()
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
