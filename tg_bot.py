from aiogram import Bot, Router, Dispatcher

from config import API_KEY_TELEGRAM

router = Router()
dp = Dispatcher()
dp.include_router(router)

bot = Bot(token=API_KEY_TELEGRAM)