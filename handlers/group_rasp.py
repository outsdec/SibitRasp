from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
import pandas as pd
from aiogram.enums import ParseMode
from keyboards.group_rasp_keyboard import BackToListGroup
import chardet
import math

import csv 

router = Router()  # [1]

csv_file_path = 'Расписание.csv'

# Detect the encoding of the CSV file
with open(csv_file_path, 'rb') as f:
    result = chardet.detect(f.read())
csv_encoding = result['encoding']

df = pd.read_csv(csv_file_path, encoding=csv_encoding, delimiter=';', on_bad_lines='skip')

# Print column names
print(df.columns)

# Correct the grouping keys as a tuple
sorted_data = df.sort_values(by=['Group', 'Day', 'Les', 'Date'])
unique_groups = sorted_data['Group'].unique()

less = {
    1: "8:30 - 10:00",
    2: "10:10 - 11:40",
    3: "12:00 - 13:30",
    4: "14:00 - 15:30",
    5: "15:40 - 17:10",
    6: "17:20 - 18:50"
}

less_type = {
    "л.": "Лекция",
    "пр.": "Практика",
    "лаб.": "Лабораторная работа",
    "конс.": "Консультация",
}

PAGE_SIZE = 10

@router.callback_query(F.data == "groups")
async def send_schedule_message(callback: types.CallbackQuery):
    try:
        page = 1
        keyboard = get_group_keyboard(page)
        total_count = len(df['Group'].unique())
        pages = math.ceil(total_count / PAGE_SIZE)
        text = f"Страница {page}/{pages}\nВыберите группу:"
        await callback.message.answer(text, reply_markup=keyboard)

    except Exception as e:
        print(e)
        await callback.message.answer("Произошла ошибка при обработке запроса.")

def get_group_keyboard(page):
    keyboard = InlineKeyboardBuilder()
    total_count = len(df['Group'].unique())
    groups = df['Group'].unique()[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]

    for group in groups:
        callback_data = f"group:{group}"
        keyboard.button(text=group, callback_data=callback_data)

    if page > 1:
        keyboard.add(InlineKeyboardButton(text="⬅️", callback_data=f"page:{page - 1}"))

    if page < math.ceil(total_count / PAGE_SIZE):
        keyboard.add(InlineKeyboardButton(text="➡️", callback_data=f"page:{page + 1}"))

    keyboard.adjust(2)
    return keyboard.as_markup()

@router.callback_query(F.data.startswith('group:'))
async def group_selected(call: types.CallbackQuery):
    selected_group = call.data.split(":")[1]
    await send_group_schedule(call.message, selected_group)

async def send_group_schedule(message, selected_group):
    try:
        group_schedule = sorted_data[sorted_data['Group'] == selected_group]

        schedule_text = f"Расписание для группы {selected_group}:\n"
        for day, day_schedule in group_schedule.groupby('Day'):
            schedule_text += f"\nДень {day}:\n"
            for index, row in day_schedule.iterrows():
                schedule_text += f"Время пары: {less.get(row['Les'])}\nПредмет: {row['Subject']}\nТип предмета: ({less_type.get(row['Subj_type'])})\nПреподаватель: {row['Name']}\nАудитория: ({row['Aud']})\n\n"

        await message.edit_text(schedule_text, parse_mode=ParseMode.MARKDOWN, reply_markup = BackToListGroup(f"page:1"))

    except Exception as e:
        print(e)
        await message.reply("Произошла ошибка при обработке запроса.")

@router.callback_query(F.data.startswith('page:'))
async def group_page_switch(call: types.CallbackQuery):
    try:
        page = int(call.data.split(":")[1])
        keyboard = get_group_keyboard(page)
        total_count = len(df['Group'].unique())
        pages = math.ceil(total_count / PAGE_SIZE)
        await list_groups(call.message, page, pages, keyboard)

    except Exception as e:
        print(e)
        await call.answer("Произошла ошибка при обработке запроса.")

async def list_groups(message, page, pages, keyboard):
    text = f"Страница {page}/{pages}\nВыберите группу:"
    await message.edit_text(text, reply_markup=keyboard)

@router.message(Command("rasp1")) 
async def send_schedule_message(message: types.Message):
    try:
        selected_group = 'ИН-40'
        
        group_schedule = sorted_data[sorted_data['Group'] == selected_group]

        schedule_text = f"Расписание для группы {selected_group}:\n"
        for day, day_schedule in group_schedule.groupby('Day'):
            for index, row in day_schedule.iterrows():
                schedule_text += f"Дата: {less.get(row['Date'])}\n Время пары: {less.get(row['Les'])}\nПредмет: {row['Subject']}\nТип предмета: ({less_type.get(row['Subj_type'])})\nПреподаватель: {row['Name']}\nАудитория: ({row['Aud']})\n\n"

        await message.answer(schedule_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        print(e)
        await message.reply("Произошла ошибка при обработке запроса.")