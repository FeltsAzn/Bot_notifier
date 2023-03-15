from aiogram import Dispatcher, Bot
from asyncio import get_event_loop
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from load_virtual_variables import TOKEN


class VolumeState(StatesGroup):
    set_volume = State()


bot = Bot(token=TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, loop=get_event_loop(), storage=storage)
