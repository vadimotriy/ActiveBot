import asyncio

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import date

from Bot.functions.ai import *
from Bot.database.constants import *
from Bot.database.database import Data
from Bot.functions.functions import make_keyboard, make_inline, color
from Bot.functions.logger import logger

router = Router()


def handlers(data: Data):
    # Стартовое сообщение
    @router.message(F.text, Command("start"))
    async def start(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("/start")

        data.set_dairy(message.from_user.id, date.today(), "very_happy", 1)
        data.set_dairy(message.from_user.id, date.today(), "happy", 2)
        data.set_dairy(message.from_user.id, date.today(), "normal", 0)
        data.set_dairy(message.from_user.id, date.today(), "sad", 1)
        data.set_dairy(message.from_user.id, date.today(), "very_sad", 0)

        try:
            data.add_user(message.from_user.id, date.today())

            keyboard = make_keyboard(ANSWERS["start"]["keyboard"], 1)
            await message.answer(text=ANSWERS["start"]["message"], reply_markup=keyboard)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Переход в меню физического благополучия
    @router.message(F.text == "Физическое благополучие")
    async def physical(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Физическое благополучие")

        try:
            inline = make_inline(ANSWERS["physical"]["inline"], ANSWERS["physical"]["backend"], 1, message.from_user.id)
            await message.answer(text=ANSWERS["physical"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Переход в главное меню
    @router.message(F.text == "Главное меню")
    async def menu(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Главное меню")

        try:
            inline = make_inline(ANSWERS["menu"]["inline"], ANSWERS["menu"]["backend"], 1, message.from_user.id)
            await message.answer(text=ANSWERS["menu"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Переход в социальное благополучие
    @router.message(F.text == "Социальное благополучие")
    async def social(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Социальное благополучие")

        try:
            inline = make_inline(ANSWERS["social"]["inline"], ANSWERS["social"]["backend"], 1, message.from_user.id)
            await message.answer(text=ANSWERS["social"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Таймер - его активация
    @router.message(Timer.reason, F.text)
    async def timer_activate(message: types.Message, state: FSMContext):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Активация таймера")

        try:
            reason = message.text
            data = await state.get_data()
            time = data["time"] // 60
            hour = False
            if time >= 60:
                time //= 60
                hour = True

            text = str(time) + (" часов" if hour else " минут")
            await state.clear()
            await message.answer(text=f"Через <b>{text}</b> вам придет напоминание. Ожидайте.")
            await asyncio.sleep(data["time"])
            await message.answer(text=ANSWERS["timer_after"]["push_message"] + reason)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Тест - ответил на 1-ый вопрос
    @router.message(Test.interests, F.text)
    async def test1(message: types.Message, state: FSMContext):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Ответил на 1-ый вопрос теста")

        try:
            await state.update_data(interests=message.text)
            await message.answer(text=ANSWERS["test"]["message2"])
            await state.set_state(Test.subjects)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Тест - ответил на 2-ой вопрос
    @router.message(Test.subjects, F.text)
    async def test2(message: types.Message, state: FSMContext):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Ответил на 2-ой вопрос теста")

        try:
            await state.update_data(subjects=message.text)
            inline = make_inline(ANSWERS["test"]["inline3"], ANSWERS["test"]["backend3"], 2, message.from_user.id)
            await message.answer(text=ANSWERS["test"]["message3"], reply_markup=inline)
            await state.set_state(Test.people)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Тест - ответил на 4-ой вопрос, финал
    @router.message(Test.problems, F.text)
    async def test4(message: types.Message, state: FSMContext):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Ответил на 4-ый вопрос теста")

        try:
            data = await state.get_data()
            interests, subjects = data["interests"], data["subjects"]
            people, problems = data["people"], message.text
            prompt = get_promt(interests, subjects, people, problems)

            await state.clear()
            await message.answer(ANSWERS["test"]["message5"])

            text = await openrouter_request(prompt=prompt, api_key=API_OPEN_ROUTER)
            await message.answer(text)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Категория психологического благополучия
    @router.message(F.text == "Психологическое благополучие")
    async def psyhology(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Психологическое благополучие")

        try:
            inline = make_inline(
                ANSWERS["psyhology"]["inline"], ANSWERS["psyhology"]["backend"], 1, message.from_user.id
            )
            await message.answer(text=ANSWERS["psyhology"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
