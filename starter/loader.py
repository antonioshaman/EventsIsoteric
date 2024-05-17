from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from starter.load_jsons import token

storage = MemoryStorage()
bot = Bot(token())

dp = Dispatcher(storage=storage)