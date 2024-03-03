from utils import create_table,new_quiz
from callbacks import dp,bot
import asyncio
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram import types,F



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = [[KeyboardButton(text='Начать игру')]]
    kb=ReplyKeyboardMarkup(keyboard=keyboard)
    # Логика обработки команды /start
    await message.answer("Привет! Я бот для проведения квиза. Введите /quiz, чтобы начать.",reply_markup=kb)




# Хэндлер на команды /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)
async def main():

    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
