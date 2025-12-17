from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Bot.database.constants import *
from Bot.database.database import Data
from Bot.database.functions import make_keyboard, make_keyboard_inline, color
from Bot.database.logger import logger

router = Router()


def handlers(data: Data):
    # Стартовое сообщение
    @router.message(F.text, Command('start'))
    async def start(message: types.Message):
        logger.info(f"Пользовтаель с {color('id=' + str(message.from_user.id))} активировал {color('/start')}")
        
        await message.answer(text=ANSWERS['start_message'])