from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove, CallbackQuery
import pandas as pd
from aiogram.enums import ParseMode
import chardet

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
sorted_data = df.sort_values(by=['Group', 'Day', 'Les'])

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
@router.message(Command("rasp")) 
async def send_schedule_message(message: types.Message):
    try:
        selected_group = 'ИН-40'
        
        group_schedule = sorted_data[sorted_data['Group'] == selected_group]

        # Формирование расписания для отправки
        schedule_text = f"Расписание для группы {selected_group}:\n"
        for day, day_schedule in group_schedule.groupby('Day'):
            schedule_text += f"\nДень {day}:\n"
            for index, row in day_schedule.iterrows():
                schedule_text += f"Время пары: {less.get(row['Les'])}\nПредмет: {row['Subject']}\nТип предмета: ({less_type.get(row['Subj_type'])})\nПреподаватель: {row['Name']}\nАудитория: ({row['Aud']})\n\n"

        await message.answer(schedule_text, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        print(e)
        await message.reply("Произошла ошибка при обработке запроса.")

@router.message(Command("sss"))  # [2]
async def cmd_start(message: Message):
    username = message.from_user.username
    user_id = message.from_user.id
    await message.answer(f'🤘 В будущем тут будет расписание.')
