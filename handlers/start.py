from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery

import csv 

router = Router()  # [1]


@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(f'🤘 В будущем тут будет расписание.')