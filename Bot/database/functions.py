from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton


def make_keyboard(buttons: list[str], adjust: int):
    builder = ReplyKeyboardBuilder()
    for i in buttons:
        builder.add(KeyboardButton(text=i))
    builder.adjust(adjust)

    return builder.as_markup()


def make_keyboard_inline(buttons: list[str], adjust: int, id: int):
    builder = InlineKeyboardBuilder()
    for i in buttons:
        builder.add(InlineKeyboardButton(text=i, callback_data=f'*{id}'))
    builder.adjust(adjust)

    return builder.as_markup()


# Функция, для желтого текста в логировании
def color(text: str):
    return f"\033[1m\033[33m{text}\033[0m"