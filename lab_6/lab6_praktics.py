from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
import requests
import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class AddNumbers(StatesGroup):
    waiting_for_first = State()
    waiting_for_second = State()

@dp.message(F.text == "/sum")
async def start_sum(message: Message, state: FSMContext):
    await message.answer("Введите первое число:")
    await state.set_state(AddNumbers.waiting_for_first)

@dp.message(AddNumbers.waiting_for_first)
async def get_first_number(message: Message, state: FSMContext):
    try:
        a = float(message.text.replace(",", "."))
        await state.update_data(a=a)
        await message.answer("Введите второе число:")
        await state.set_state(AddNumbers.waiting_for_second)
    except ValueError:
        await message.answer("Введите корректное число, например 5.2")

@dp.message(AddNumbers.waiting_for_second)
async def get_second_number(message: Message, state: FSMContext):
    try:
        b = float(message.text.replace(",", "."))
        data = await state.get_data()
        a = data["a"]

        try:
            response = requests.get("http://localhost:5001/add", params={"a": a, "b": b})
            res_json = response.json()

            if 'sum' in res_json:
                await message.answer(f"Сумма: {res_json['sum']}")
            else:
                await message.answer(f"Ошибка: {res_json.get('error', 'Неизвестная ошибка')}")
        except requests.exceptions.RequestException as e:
            await message.answer(f"Ошибка при подключении к сервису: {e}")

        await state.clear()
    except ValueError:
        await message.answer("Введите корректное число, например 7")


import asyncio

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())