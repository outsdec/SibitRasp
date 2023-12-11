from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_menu():
    menu = [
        [
            InlineKeyboardButton(text="По группам", callback_data="groups"),
        ],
        [
            InlineKeyboardButton(text="По аудиториям", callback_data="audiences")
        ],
        [
            InlineKeyboardButton(text="По преподавателям", callback_data="teachers")
        ]
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu