from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_row_keyboard(items):
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_column_keyboard(items):
    column = [KeyboardButton(text=item) for item in items]
    builder = ReplyKeyboardBuilder()
    for item in column:
        builder.add(item)
        builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
