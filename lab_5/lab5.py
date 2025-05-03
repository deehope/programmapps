import os
import asyncio
import psycopg2
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

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
