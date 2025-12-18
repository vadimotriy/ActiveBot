from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from random import choice

from Bot.database.constants import *
from Bot.database.database import Data
from Bot.database.functions import color, make_inline, get_days
from Bot.database.logger import logger

router_for_callbacks = Router()

def callbacks(data: Data):
    # Ежедневные задания (физическое благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*tasks*"))
    async def tasks(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Ежедневные задания")

        try:
            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
    
    # Настройки (главное меню)
    @router_for_callbacks.callback_query(F.data.startswith("*settings*"))
    async def settings(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Настройки")

        try:
            settings = data.get_settings(id_user)
            text1 = ("включить" if settings[0] == 0 else "выключить") + " задания на плавание"
            answer_text1 = (("❌" if settings[0] == 0 else "✅") + 
            " задания на плавание <b>" + ("отключены" if settings[0] == 0 else "включены") + "</b>\n")
            text2 = ("включить" if settings[1] == 0 else "выключить") + " задания на велосипед"
            answer_text2 = (("❌" if settings[1] == 0 else "✅") + 
            " задания на велосипед <b>" + ("отключены" if settings[1] == 0 else "включены") + "</b>\n")

            buttons = [text1, text2] + ANSWERS["settings"]["inline"]
            inline = make_inline(buttons, ANSWERS["settings"]["backend"], 1, id_user)

            text = ANSWERS["settings"]["message"] + answer_text1 + answer_text2
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
    
    # Изменние настроек о добавление плавания в ежедневные задания
    @router_for_callbacks.callback_query(F.data.startswith("*swimming*"))
    async def swimming(callback_query: types.CallbackQuery):
        text = callback_query.data.split("*")
        id_user, change = int(text[2]), text[1]
        index = 0 if change == "swimming" else 1
        user_id = color("id=" + str(id_user))
        command = color("Изменение настроек")

        try:
            settings = data.get_settings(id_user)
            data.change_settings(id_user, change.upper(), int(not bool(settings[index])))

            settings = data.get_settings(id_user)
            text1 = ("включить" if settings[0] == 0 else "выключить") + " задания на плавание"
            answer_text1 = (("❌" if settings[0] == 0 else "✅") + 
            " задания на плавание <b>" + ("отключены" if settings[0] == 0 else "включены") + "</b>\n")
            text2 = ("включить" if settings[1] == 0 else "выключить") + " задания на велосипед"
            answer_text2 = (("❌" if settings[1] == 0 else "✅") + 
            " задания на велосипед <b>" + ("отключены" if settings[1] == 0 else "включены") + "</b>\n")

            buttons = [text1, text2] + ANSWERS["settings"]["inline"]
            inline = make_inline(buttons, ANSWERS["settings"]["backend"], 1, id_user)

            text = ANSWERS["settings"]["message"] + answer_text1 + answer_text2
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
    
    # Изменние настроек о добавление велосипеда в ежедневные задания
    @router_for_callbacks.callback_query(F.data.startswith("*bicycle*"))
    async def bicycle(callback_query: types.CallbackQuery):
        text = callback_query.data.split("*")
        id_user, change = int(text[2]), text[1]
        index = 0 if change == "swimming" else 1
        user_id = color("id=" + str(id_user))
        command = color("Изменение настроек")

        try:
            settings = data.get_settings(id_user)
            data.change_settings(id_user, change.upper(), int(not bool(settings[index])))

            settings = data.get_settings(id_user)
            text1 = ("включить" if settings[0] == 0 else "выключить") + " задания на плавание"
            answer_text1 = (("❌" if settings[0] == 0 else "✅") + 
            " задания на плавание <b>" + ("отключены" if settings[0] == 0 else "включены") + "</b>\n")
            text2 = ("включить" if settings[1] == 0 else "выключить") + " задания на велосипед"
            answer_text2 = (("❌" if settings[1] == 0 else "✅") + 
            " задания на велосипед <b>" + ("отключены" if settings[1] == 0 else "включены") + "</b>\n")

            buttons = [text1, text2] + ANSWERS["settings"]["inline"]
            inline = make_inline(buttons, ANSWERS["settings"]["backend"], 1, id_user)

            text = ANSWERS["settings"]["message"] + answer_text1 + answer_text2
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
    
    # Данные о статистике
    @router_for_callbacks.callback_query(F.data.startswith("*statistics*"))
    async def statistics(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Статистика")

        try:
            settings = data.get_settings(id_user)
            registration = f"Дата регистрации в боте: <i>{settings[2]}</i>\n"
            days = f"Дней в сервисе: <i>{get_days(settings[2])}</i>\n"
            tasks = f"Выполнено ежедневных заданий: <i>0</i>"

            text = ANSWERS["statistics"]["message"] + registration + days + tasks
            inline = make_inline(ANSWERS["statistics"]["inline"], ANSWERS["statistics"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
    
    # возвращение в главное меню (из настроек)
    @router_for_callbacks.callback_query(F.data.startswith("*menu*"))
    async def menu_back(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Возвращение в главное меню")

        try:
            inline = make_inline(ANSWERS["menu"]["inline"], ANSWERS["menu"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["menu"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
    
    # советы (физическое благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*advices*"))
    async def advices(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Советы")

        try:
            advice = choice(ADVICES)
            await callback_query.answer(text=advice, show_alert=True)

            logger.info(f"Пользователь с {user_id} активировал {command}")
        
        except Exception as e: # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")