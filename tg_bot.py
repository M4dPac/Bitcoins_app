import asyncio
import logging
import sys

from aiogram import Bot, Router, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config import API_KEY_TELEGRAM

router = Router()
dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f'Привет {message.from_user.full_name}, я твой бот-криптокошелек, \n'
        'у меня ты можешь хранить и отправлять биткоины')


@dp.message(Command(commands=["help"]))
async def help_(message: Message):
    await message.answer("Help!")


async def main():
    bot = Bot(token=API_KEY_TELEGRAM)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
