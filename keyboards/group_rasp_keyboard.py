from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def BackToListGroup(back):
    menu = [
        [
            InlineKeyboardButton(text="🔙 Вернуться назад", callback_data=f"{back}"),
        ],
    ]
    menu = InlineKeyboardMarkup(inline_keyboard=menu)
    return menu