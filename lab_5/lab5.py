import os
import asyncio
import psycopg2
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup
'''
# Подключение к базе данных
conn = psycopg2.connect(
    dbname="Bot_5",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Создание курсора
cur = conn.cursor()

# Создание таблицы currencies
cur.execute("""
CREATE TABLE IF NOT EXISTS currencies (
    id INTEGER PRIMARY KEY,
    currency_name VARCHAR,
    rate NUMERIC
)
""")

# Создание таблицы admins
cur.execute("""
CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY,
    chat_id VARCHAR
)
""")

# Сохранение изменений и закрытие соединения
conn.commit()
cur.close()
conn.close()
'''

# Загрузка токена из .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Подключение к БД
def get_connection():
    return psycopg2.connect(
        dbname="Bot_5",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

# Проверка на администратора
def is_admin(chat_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM admins WHERE chat_id = %s", (str(chat_id),))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

class CurrencyStates(StatesGroup):
    waiting_for_name_add = State()
    waiting_for_rate_add = State()
    waiting_for_name_delete = State()
    waiting_for_name_update = State()
    waiting_for_new_rate = State()
    waiting_for_currency_name_convert = State()
    waiting_for_amount_convert = State()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start(message: types.Message):
    if is_admin(message.chat.id):
        await message.answer(
            "Вы являетесь администратором бота Bot_5\n"
            "Доступные команды:\n"
            "/manage_currency - управление валютами\n"
            "/get_currencies - список всех валют\n"
            "/convert - конвертировать валюту в рубли"
        )
    else:
        await message.answer(
            "Доступные команды:\n"
            "/get_currencies - список всех валют\n"
            "/convert - конвертировать валюту в рубли"
        )

# Команда /manage_currency
@dp.message(F.text == "/manage_currency")
async def manage_currency(message: Message):
    if not is_admin(message.chat.id):
        await message.answer("Нет доступа к команде")
        return

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text="Добавить валюту"),
            KeyboardButton(text="Удалить валюту"),
            KeyboardButton(text="Изменить курс валюты")
        ]],
        resize_keyboard=True
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Добавление валюты
@dp.message(F.text == "Добавить валюту")
async def ask_currency_name_add(message: Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await state.set_state(CurrencyStates.waiting_for_name_add)

@dp.message(CurrencyStates.waiting_for_name_add)
async def check_currency_exists(message: Message, state: FSMContext):
    name = message.text.upper()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
    exists = cur.fetchone()
    cur.close()
    conn.close()

    if exists:
        await message.answer("Данная валюта уже существует.")
        await state.clear()
    else:
        await state.update_data(name=name)
        await message.answer("Введите курс к рублю:")
        await state.set_state(CurrencyStates.waiting_for_rate_add)

@dp.message(CurrencyStates.waiting_for_rate_add)
async def save_currency(message: Message, state: FSMContext):
    try:
        rate = float(message.text.replace(",", "."))
        data = await state.get_data()
        name = data["name"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM currencies")
        new_id = cur.fetchone()[0]
        cur.execute("INSERT INTO currencies (id, currency_name, rate) VALUES (%s, %s, %s)", (new_id, name, rate))
        conn.commit()
        cur.close()
        conn.close()

        await message.answer(f"Валюта: {name} успешно добавлена.")
    except ValueError:
        await message.answer("Введите корректное число.")
    finally:
        await state.clear()

# Удаление валюты
@dp.message(F.text == "Удалить валюту")
async def ask_currency_name_delete(message: Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await state.set_state(CurrencyStates.waiting_for_name_delete)

@dp.message(CurrencyStates.waiting_for_name_delete)
async def delete_currency(message: Message, state: FSMContext):
    name = message.text.upper()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM currencies WHERE currency_name = %s", (name,))
    deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        await message.answer(f"Валюта {name} удалена.")
    else:
        await message.answer("Такая валюта не найдена.")
    await state.clear()

# Обновление курса
@dp.message(F.text == "Изменить курс валюты")
async def ask_currency_name_update(message: Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await state.set_state(CurrencyStates.waiting_for_name_update)

@dp.message(CurrencyStates.waiting_for_name_update)
async def ask_new_rate(message: Message, state: FSMContext):
    name = message.text.upper()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM currencies WHERE currency_name = %s", (name,))
    exists = cur.fetchone()
    cur.close()
    conn.close()

    if not exists:
        await message.answer("Такая валюта не найдена.")
        await state.clear()
    else:
        await state.update_data(name=name)
        await message.answer("Введите новый курс к рублю:")
        await state.set_state(CurrencyStates.waiting_for_new_rate)

@dp.message(CurrencyStates.waiting_for_new_rate)
async def update_rate(message: Message, state: FSMContext):
    try:
        rate = float(message.text.replace(",", "."))
        data = await state.get_data()
        name = data["name"]

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE currencies SET rate = %s WHERE currency_name = %s", (rate, name))
        conn.commit()
        cur.close()
        conn.close()

        await message.answer(f"Курс валюты {name} обновлён.")
    except ValueError:
        await message.answer("Введите корректное число.")
    finally:
        await state.clear()

@dp.message(F.text == "/get_currencies")
async def get_currencies(message: Message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT currency_name, rate FROM currencies ORDER BY currency_name")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if not rows:
        await message.answer("Список валют пуст.")
    else:
        text = "\n".join([f"{name} — {rate}" for name, rate in rows])
        await message.answer(text)

# Конвертация валюты
@dp.message(F.text == "/convert")
async def start_convert(message: Message, state: FSMContext):
    await message.answer("Введите название валюты:")
    await state.set_state(CurrencyStates.waiting_for_currency_name_convert)

@dp.message(CurrencyStates.waiting_for_currency_name_convert)
async def get_currency_for_convert(message: Message, state: FSMContext):
    name = message.text.upper()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT rate FROM currencies WHERE currency_name = %s", (name,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result is None:
        await message.answer("Такая валюта не найдена.")
        await state.clear()
    else:
        await state.update_data(name=name, rate=result[0])
        await message.answer("Введите сумму:")
        await state.set_state(CurrencyStates.waiting_for_amount_convert)

@dp.message(CurrencyStates.waiting_for_amount_convert)
async def convert_to_rubles(message: Message, state: FSMContext):
    try:
        amount = float(message.text.replace(",", "."))
        data = await state.get_data()
        name = data["name"]
        rate = data["rate"]
        rubles = amount * float(rate)

        await message.answer(f"{amount} {name} = {rubles:.2f} RUB")
    except ValueError:
        await message.answer("Введите корректное число.")
    finally:
        await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




