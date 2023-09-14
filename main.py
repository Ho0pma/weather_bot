from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from handlers.main import register_all_handlers
from misc.env import TgKeys


async def __on_start_up(dp: Dispatcher) -> None:
    print('The bot has started')
    register_all_handlers(dp)


def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)

