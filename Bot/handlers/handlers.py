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
            logger.info(f"Пользовтаель с {user_id} активировал {command}")
            keyboard = make_keyboard(ANSWERS["start"]["keyboard"], 1)

            await message.answer(text=ANSWERS["start"]["message"], reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Пользовтаель с {user_id} активировал {command}\nОшибка: {e}")