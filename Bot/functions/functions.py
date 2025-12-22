import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton
from random import randint, choice

from Bot.database.database import Data
from Bot.database.constants import TASKS, BASE_PROMT

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

# Функция для желтого текста в логировании
def color(text: str) -> str:
    return f"\033[1m\033[33m{text}\033[0m"

# Функция для нахождения количества дней в промежутке
def get_days(registration: str) -> int:
    date_now = datetime.date.today()

    datetime_object = datetime.datetime.strptime(registration, "%Y-%m-%d")
    date_object = datetime_object.date()

    return (date_now - date_object).days + 1

# Функция для поиска заданий пользователя на сегодняшний день
def get_tasks(user_id: int, data: Data) -> tuple:
    date_now = datetime.date.today()
    result = data.get_tasks(user_id, date_now)

    if not result:
        generate_tasks(user_id, data, date_now)
        result = data.get_tasks(user_id, date_now)

    return result[0]

# Функция для генерации новых ежедневных заданий
def generate_tasks(user_id: int, data: Data, date: str):
    res, num = {}, 0
    settings = data.get_settings(user_id)

    # добавление заданий на плавание с шансом 20%
    if settings[0] and randint(1, 5) == 2:
        res[3] = choice(TASKS["distance"][2])
        num += 1

    # добавление заданий на велосипед с шансом 20%
    if settings[1] and randint(1, 5) == 3:
        res[2] = choice(TASKS["distance"][3])
        num += 1

    if num == 0:
        res[randint(1, 3)] = choice(TASKS["distance"][randint(0, 1)])

    for i in range(1, 4):
        if not res.get(i, 0):
            res[i] = choice(TASKS["exercise"][randint(0, 3)])
    
    res_list = []
    for i in range(1, 4):
        task = res[i]
        res_list.append(task["activity"].capitalize() + " – " + task["description"].lower())
    
    data.add_tasks(user_id, date, res_list)

