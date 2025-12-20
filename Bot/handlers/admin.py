import asyncio

from aiogram import types, F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import date

from Bot.functions.ai import *
from Bot.database.constants import *
from Bot.database.database import Data
from Bot.functions.functions import make_keyboard, make_inline, color
from Bot.functions.logger import logger

router_for_admin = Router()


def admin(data: Data, bot: Bot):
    # Днневное апоминание об ежедневных заданий
    # Срабатывает если пользователь не выполнил ни одного задания
    @router_for_admin.message(F.text, Command("push_day"))
    async def push_day(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("/push_day")

        try:
            if str(message.from_user.id) != ADMIN:
                await message.answer(text=ANSWERS["push"]["message_not_admin"])
            else:
                all_users = data.get_all_id()

                date_now = date.today()
                num = 0
                for i in all_users:
                    info = data.get_tasks(i[0], date_now)
                    if info:
                        info = info[0]
                        if all((not info[1], not info[3], not info[5])):
                            await bot.send_message(chat_id=i[0], text=ANSWERS["push"]["message_day"])
                            num += 1
                    else:
                        await bot.send_message(chat_id=i[0], text=ANSWERS["push"]["message_day"])
                        num += 1


                await message.answer(text=ANSWERS["push"]["message_admin"] + f"{num} сообщений.")
                logger.info(f"АДМИН с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"АДМИН с {user_id} активировал {command}\nОшибка: {e}")
    
    # Вечернее апоминание об ежедневных заданий
    # Срабатывает если пользователь не выполнил хотя бы одно задание
    @router_for_admin.message(F.text, Command("push_evening"))
    async def push_day(message: types.Message):
        user_id = color("id=" + str(message.from_user.id))
        command = color("/push_evening")

        try:
            if str(message.from_user.id) != ADMIN:
                await message.answer(text=ANSWERS["push"]["message_not_admin"])
            else:
                all_users = data.get_all_id()

                date_now = date.today()
                num = 0
                for i in all_users:
                    info = data.get_tasks(i[0], date_now)
                    if info:
                        info = info[0]
                        if all((not info[1], not info[3], not info[5])):
                            await bot.send_message(chat_id=i[0], text=ANSWERS["push"]["message_day"])
                            num += 1
                        elif any((not info[1], not info[3], not info[5])):
                            await bot.send_message(chat_id=i[0], text=ANSWERS["push"]["message_evening"])
                            num += 1
                    else:
                        await bot.send_message(chat_id=i[0], text=ANSWERS["push"]["message_day"])
                        num += 1


                await message.answer(text=ANSWERS["push"]["message_admin"] + f"{num} сообщений.")
                logger.info(f"АДМИН с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"АДМИН с {user_id} активировал {command}\nОшибка: {e}")