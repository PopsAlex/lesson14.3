from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ('7599316396:AAFZ_04i945YF9lgxvaYunIxvA9ztdWzQlA')
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.insert(button)
kb.insert(button2)
kb.add(button3)


kb_inline = InlineKeyboardMarkup()
button_inline = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_inline2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inline.insert(button_inline)
kb_inline.insert(button_inline2)


kb_inline_product = InlineKeyboardMarkup()
button_inline_product1 = InlineKeyboardButton(text='Волжанка', callback_data='product_buying')
button_inline_product2 = InlineKeyboardButton(text='Бодрянка', callback_data='product_buying')
button_inline_product3 = InlineKeyboardButton(text='Ульянка', callback_data='product_buying')
button_inline_product4 = InlineKeyboardButton(text='Герольштайнер', callback_data='product_buying')
kb_inline_product.add(button_inline_product1, button_inline_product2, button_inline_product3,
                      button_inline_product4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

product = ('volzhanka', 'bodryanka', 'ulyanka', 'gerolstayner')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_inline)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f'10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    cal = 10 * float(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {cal}')
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    index = 0
    for i in product:
        index += 1
        with open(f'photo/{i}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Product{index} | Описание: вода {i} | Цена: {index * 100}')
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_inline_product)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрили продукт!')
    await call.answer()


@dp.message_handler()
async def all_message(message):
       await message.answer('Введите команду /start, чтобы начать общение')



if __name__ == '__main__':
       executor.start_polling(dp, skip_updates=True)