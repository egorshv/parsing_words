from aiogram.dispatcher.filters.state import State, StatesGroup


class AddUrl(StatesGroup):
    url = State()


class GenerateFile(StatesGroup):
    name = State()