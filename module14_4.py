import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from config import *
from keyboards import *
import crud_functions

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text=['Регистрация'])
async def sign_up(message):
    await message.answer("Введите имя пользователя(только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    user_included = crud_functions.is_included(message.text)
    if user_included:
        await message.answer('Пользователь существует, введите другое имя')
        await RegistrationState.username.set()
        return
    await state.update_data(username=message.text)
    await message.answer("Введите свой email")
    await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст")
    await RegistrationState.age.set()

@dp.message_handler(state= RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Регистрация прошла успешно')
    await state.finish()


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию", reply_markup=inline_menu)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) - 161")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    a = int(data["weight"])
    b = int(data["growth"])
    c = int(data["age"])
    norma = 10 * a + 6.25 * b - 5 * c + -161
    await message.answer(f'Ваша норма калорий {norma}')
    await state.finish()


@dp.message_handler(text=["Купить"])
async def get_buying_list(message: types.Message):
    products = get_all_products()
    if products:
        for product in products:
            product_id, title, description, price = product
            image_path = f'/Users/Shared/Previously Relocated Items/Security/Рабочая/Pyton/Project13/{product_id}.png'
            try:
                with open(image_path, "rb") as img:
                    await message.answer_photo(img, f'Название: {title} | Описание: {description} | Цена: {price}р')
            except FileNotFoundError:
                await message.answer(f'Изображение для продукта "{title}" не найдено.')
        await message.answer('Выберите продукт для покупки:', reply_markup=inline_menu_product)
    else:
        await message.answer('На данный момент нет доступных продуктов.')


@dp.callback_query_handler(text="product_buying")
async def end_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f"Привет! Я бот помогающий твоему здоровью.", reply_markup=start_menu)


@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
