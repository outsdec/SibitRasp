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
print(df.columns)

sorted_data = df.sort_values(by=['Group', 'Day', 'Les', 'Date', 'Aud'])
unique_audiences = sorted_data['Aud'].unique()

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

@router.callback_query(F.data == "audiences")
async def send_schedule_message(callback: types.CallbackQuery):
    try:
        page = 1
        keyboard = get_audiences_keyboard(page)
        total_count = len(df['Aud'].unique())
        pages = math.ceil(total_count / PAGE_SIZE)
        text = f"Страница {page}/{pages}\nВыберите аудиторию:"
        await callback.message.answer(text, reply_markup=keyboard)

    except Exception as e:
        print(e)
        await callback.message.answer("Произошла ошибка при обработке запроса.")

def get_audiences_keyboard(page):
    keyboard = InlineKeyboardBuilder()
    total_count = len(df['Aud'].unique())
    audiences = df['Aud'].unique()[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]

    for audience in audiences:
        callback_data = f"audiences:{audience}"
        keyboard.button(text=audience, callback_data=callback_data)

    if page > 1:
        keyboard.add(InlineKeyboardButton(text="⬅️", callback_data=f"pages:{page - 1}"))

    if page < math.ceil(total_count / PAGE_SIZE):
        keyboard.add(InlineKeyboardButton(text="➡️", callback_data=f"pages:{page + 1}"))

    keyboard.adjust(2)
    return keyboard.as_markup()

@router.callback_query(F.data.startswith('audiences:'))
async def audiences_selected(call: types.CallbackQuery):
    selected_audience = call.data.split(":")[1]
    await send_audience_schedule(call.message, selected_audience)

async def send_audience_schedule(message, selected_audience):
    try:
        audience_schedule = sorted_data[sorted_data['Aud'] == selected_audience]

        schedule_text = f"Расписание для аудитории {selected_audience}:\n"
        for day, day_schedule in audience_schedule.groupby('Day'):
            schedule_text += f"\nДень {day}:\n"
            for index, row in day_schedule.iterrows():
                schedule_text += f"Группы: {row['Group']}\nВремя пары: {less.get(row['Les'])}\nПредмет: {row['Subject']}\nТип предмета: ({less_type.get(row['Subj_type'])})\nПреподаватель: {row['Name']}\nАудитория: ({row['Aud']})\n\n"

        await message.edit_text(schedule_text, parse_mode=ParseMode.MARKDOWN, reply_markup = BackToListGroup(f"pages:1"))

    except Exception as e:
        print(e)
        await message.reply("Произошла ошибка при обработке запроса.")

@router.callback_query(F.data.startswith('pages:'))
async def audience_page_switch(call: types.CallbackQuery):
    try:
        page = int(call.data.split(":")[1])
        keyboard = get_audiences_keyboard(page)
        total_count = len(df['Aud'].unique())
        pages = math.ceil(total_count / PAGE_SIZE)
        await list_audiences(call.message, page, pages, keyboard)

    except Exception as e:
        print(e)
        await call.answer("Произошла ошибка при обработке запроса.")

async def list_audiences(message, page, pages, keyboard):
    text = f"Страница {page}/{pages}\nВыберите группу:"
    await message.edit_text(text, reply_markup=keyboard)
