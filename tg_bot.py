import asyncio
import logging
import sys

from aiogram import Bot, Router, Dispatcher
from aiogram import F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BotCommand

import config
from config import API_KEY_TELEGRAM

router = Router()
dp = Dispatcher()
dp.include_router(router)
bot = Bot(token=API_KEY_TELEGRAM)


def create_keyboard(*args, row_width=2):
    tmp = [KeyboardButton(text=key) for key in args]
    keys = [tmp[i:i + row_width] for i in range(0, len(args), row_width)]
    return ReplyKeyboardMarkup(keyboard=keys, resize_keyboard=True)


# Общее меню
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот-криптокошелек, \n'
        'у меня ты можешь хранить и отправлять биткоины')

    await command_menu_handler(message)


@dp.message(F.text == 'Меню')
async def command_menu_handler(message: Message):
    text = 'Выберите действие'
    markup = create_keyboard('Кошелёк', 'Перевести', 'История')

    await message.answer(text=text, reply_markup=markup)


@dp.message(F.text == 'Кошелёк')
async def command_wallet_handler(message: Message):
    markup = create_keyboard('Меню')

    balance = 0.0
    text = f'Ваш баланс: {balance}'
    await message.answer(text, reply_markup=markup)


@dp.message(F.text == 'Перевести')
async def command_transfer_handler(message: Message):
    markup = create_keyboard('Меню')
    text = 'Введите адрес кошелька для перевода'
    await message.answer(text, reply_markup=markup)


@dp.message(F.text == 'История')
async def command_history_handler(message: Message):
    markup = create_keyboard('Меню')
    transactions = ['1', '2', '3']
    text = 'Ваша история переводов: \n' + '\n'.join(transactions)
    await message.answer(text, reply_markup=markup)


# Меню администратора
@dp.message(F.from_user.id == config.TG_ADMIN_ID and F.text == 'админ')
async def command_admin_handler(message: Message):
    markup = create_keyboard('Общий баланс', 'Все пользователи', 'Данные пользователя', 'Удалить пользователя')
    text = 'Админ панель'
    await message.answer(text, reply_markup=markup)


# Запуск бота
@dp.message()
async def message_handler(message: Message):
    print(message.model_dump_json(indent=4, exclude_none=True))


async def setup_bot_commands():
    bot_commands = [
        BotCommand(command='/start', description='Запустить бота')
    ]
    await bot.set_my_commands(bot_commands)


async def main():
    await dp.start_polling(bot, on_startup=setup_bot_commands)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
