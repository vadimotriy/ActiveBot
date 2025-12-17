from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Bot.database.constants import *
from Bot.database.database import Data
from Bot.database.functions import make_keyboard, make_inline, color
from Bot.database.logger import logger

router = Router()


def handlers(data: Data):
    # Стартовое сообщение
    @router.message(F.text, Command("start"))
    async def start(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("/start")

        try:
            data.add_user(message.from_user.id)
            
            keyboard = make_keyboard(ANSWERS["start"]["keyboard"], 1)
            await message.answer(text=ANSWERS["start"]["message"], reply_markup=keyboard)

            logger.info(f"Пользовтаель с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользовтаель с {user_id} активировал {command}\nОшибка: {e}")
    
    # Переход в меню физического благополучия
    @router.message(F.text == "Физическое благополучие")
    async def physical(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Физическое благополучие")

        try:
            inline = make_inline(ANSWERS["physical"]["inline"], ANSWERS["physical"]["backend"], 1, message.from_user.id)
            await message.answer(text=ANSWERS["physical"]["message"], reply_markup=inline)

            logger.info(f"Пользовтаель с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользовтаель с {user_id} активировал {command}\nОшибка: {e}")
    
    # Переход в главное меню
    @router.message(F.text == "Главное меню")
    async def menu(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("Главное меню")

        try:
            inline = make_inline(ANSWERS["menu"]["inline"], ANSWERS["menu"]["backend"], 1, message.from_user.id)
            await message.answer(text=ANSWERS["menu"]["message"], reply_markup=inline)

            logger.info(f"Пользовтаель с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользовтаель с {user_id} активировал {command}\nОшибка: {e}")