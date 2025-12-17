from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton


# Функция для создания клавиатуры
def make_keyboard(buttons: list[str], adjust: int):
    builder = ReplyKeyboardBuilder()
    for i in buttons:
        builder.add(KeyboardButton(text=i))
    builder.adjust(adjust)

    return builder.as_markup()


# Функция для создания инлайн кнопок
def make_inline(buttons: list[str], message: list[str], adjust: int, id: int):
    builder = InlineKeyboardBuilder()
    for i in range(len(buttons)):
        builder.add(InlineKeyboardButton(text=buttons[i], callback_data=f'*{message[i]}*{id}'))
    builder.adjust(adjust)

    return builder.as_markup()


# Функция, для желтого текста в логировании
def color(text: str) -> str:
    return f"\033[1m\033[33m{text}\033[0m"