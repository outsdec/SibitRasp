from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
import csv 
from keyboards.start_keyboard import start_menu


router = Router()  # [1]

@router.message(Command("start"))  # [2]
async def cmd_start(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(f'📚 Меню расписания СИБИТ.\n\n На кнопках предоставлены категории расписания, нажмите на нужную.', reply_markup=start_menu())
