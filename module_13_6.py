from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


# Создание группы состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Создание клавиатуры
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton('Рассчитать')
button_info = types.KeyboardButton('Информация')
keyboard.add(button_calculate, button_info)

# Создание Inline-клавиатуры
inline_keyboard = InlineKeyboardMarkup()
button_inline_calories = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_inline_formulas = InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
inline_keyboard.add(button_inline_calories, button_inline_formulas)


# Приветствие при нажатии START
@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. Выберите действие:", reply_markup=keyboard)


# Функция для отправки Inline меню при нажатии на кнопку 'Рассчитать'
@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=inline_keyboard)


# Функция для обработки нажатия кнопки с формулами
@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer(
        "Формула Миффлина-Сан Жеора:\n10 × вес (кг) + 6.25 × рост (см) - 5 × возраст (годы) + 5 (для мужчин) или -161 (для женщин).")
    await call.answer()  # Закрывает всплывающее окно уведомления


# Функция для обработки команды и начала ввода возраста
@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()  # Закрывает всплывающее окно уведомления


# Функция для обработки состояния возраста и запроса роста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# Функция для обработки состояния роста и запроса веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


# Функция для обработки состояния веса и подсчета калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    # Расчет калорий по формуле Миффлина - Сан Жеора (для мужчин)
    calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5  # Формула для мужчин

    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал в день.')
    await state.finish()


# Общий обработчик для всех остальных сообщений
@dp.message_handler()
async def default_response(message: types.Message):
    await message.answer('Введите команду /start')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
