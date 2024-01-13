import asyncio
import logging
import sys

from aiogram import Bot, Router, Dispatcher
from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import config
from config import API_KEY_TELEGRAM

router = Router()
dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот-криптокошелек, \n'
        'у меня ты можешь хранить и отправлять биткоины')

    await command_menu_handler(message)


@dp.message(F.text, Command('Меню', prefix='!'))
async def command_menu_handler(message: Message):
    btn1 = KeyboardButton(text='!Кошелёк')
    btn2 = KeyboardButton(text='!Перевести')
    btn3 = KeyboardButton(text='!История')
    array_buttons = [[btn1, btn2], [btn3]]

    markup = ReplyKeyboardMarkup(keyboard=array_buttons, resize_keyboard=True)

    await message.answer(text='Выберите действие', reply_markup=markup)


@dp.message(F.text, Command('Кошелёк', prefix='!'))
async def command_wallet_handler(message: Message):
    btn1 = KeyboardButton(text='!Меню')
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)

    balance = 0.0
    text = f'Ваш баланс: {balance}'
    await message.answer(text, reply_markup=markup)


@dp.message(F.text, Command('Перевести', prefix='!'))
async def command_transfer_handler(message: Message):
    btn1 = KeyboardButton(text='!Меню')
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    text = 'Введите адрес кошелька для перевода'
    await message.answer(text, reply_markup=markup)


@dp.message(F.text, Command('История', prefix='!'))
async def command_history_handler(message: Message):
    btn1 = KeyboardButton(text='!Меню')
    markup = ReplyKeyboardMarkup(keyboard=[[btn1]], resize_keyboard=True)
    transactions = ['1', '2', '3']
    text = 'Ваша история переводов: \n' + '\n'.join(transactions)
    await message.answer(text, reply_markup=markup)


@dp.message(F.from_user.id == config.TG_ADMIN_ID,
            Command('Админ', prefix='!', ignore_case=True))
async def command_admin_handler(message: Message):
    await message.answer('Ты админ')


@dp.message(F.text)
async def message_handler(message: Message):
    await message.answer(f'Ты написал: {message.from_user.id}')
    print(type(config.TG_ADMIN_ID), type(message.from_user.id))


async def main():
    bot = Bot(token=API_KEY_TELEGRAM)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
