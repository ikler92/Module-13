from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


# Создание группы состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

# Приветствие при нажатии START
@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью.")


# Функция для обработки команды и начала ввода возраста
@dp.message_handler(text='Calories')
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


# Функция для обработки состояния возраста и запроса роста
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# Функция для обработки состояния роста и запроса веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


# Функция для обработки состояния веса и подсчета калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    # Расчет калорий по формуле Миффлина - Сан Жеора (для мужчин)
    calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5  # Формула для мужчин

    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал в день.')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
