from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from datetime import date
from random import choice

from Bot.database.constants import *
from Bot.database.database import Data
from Bot.functions.functions import color, get_days, get_tasks, make_inline
from Bot.functions.logger import logger

router_for_callbacks = Router()


def callbacks(data: Data):
    main_menu(data)
    physical_well_being(data)
    social_well_being(data)
    psyhological_well_being(data)


def main_menu(data: Data):
    # Настройки (главное меню)
    @router_for_callbacks.callback_query(F.data.startswith("*settings*"))
    async def settings(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Настройки")

        try:
            settings = data.get_settings(id_user)
            text1 = ("включить" if settings[0] == 0 else "выключить") + " задания на плавание"
            answer_text1 = (
                ("❌" if settings[0] == 0 else "✅")
                + " задания на плавание <b>"
                + ("отключены" if settings[0] == 0 else "включены")
                + "</b>\n"
            )
            text2 = ("включить" if settings[1] == 0 else "выключить") + " задания на велосипед"
            answer_text2 = (
                ("❌" if settings[1] == 0 else "✅")
                + " задания на велосипед <b>"
                + ("отключены" if settings[1] == 0 else "включены")
                + "</b>\n"
            )

            buttons = [text1, text2] + ANSWERS["settings"]["inline"]
            inline = make_inline(buttons, ANSWERS["settings"]["backend"], 1, id_user)

            text = ANSWERS["settings"]["message"] + answer_text1 + answer_text2
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Изменение настроек о добавление плавания в ежедневные задания
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
            answer_text1 = (
                ("❌" if settings[0] == 0 else "✅")
                + " задания на плавание <b>"
                + ("отключены" if settings[0] == 0 else "включены")
                + "</b>\n"
            )
            text2 = ("включить" if settings[1] == 0 else "выключить") + " задания на велосипед"
            answer_text2 = (
                ("❌" if settings[1] == 0 else "✅")
                + " задания на велосипед <b>"
                + ("отключены" if settings[1] == 0 else "включены")
                + "</b>\n"
            )

            buttons = [text1, text2] + ANSWERS["settings"]["inline"]
            inline = make_inline(buttons, ANSWERS["settings"]["backend"], 1, id_user)

            text = ANSWERS["settings"]["message"] + answer_text1 + answer_text2
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Изменение настроек о добавление велосипеда в ежедневные задания
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
            answer_text1 = (
                ("❌" if settings[0] == 0 else "✅")
                + " задания на плавание <b>"
                + ("отключены" if settings[0] == 0 else "включены")
                + "</b>\n"
            )
            text2 = ("включить" if settings[1] == 0 else "выключить") + " задания на велосипед"
            answer_text2 = (
                ("❌" if settings[1] == 0 else "✅")
                + " задания на велосипед <b>"
                + ("отключены" if settings[1] == 0 else "включены")
                + "</b>\n"
            )

            buttons = [text1, text2] + ANSWERS["settings"]["inline"]
            inline = make_inline(buttons, ANSWERS["settings"]["backend"], 1, id_user)

            text = ANSWERS["settings"]["message"] + answer_text1 + answer_text2
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Данные о статистике
    @router_for_callbacks.callback_query(F.data.startswith("*statistics*"))
    async def statistics(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Статистика")

        try:
            settings = data.get_settings(id_user)
            dairy = data.get_dairy(id_user)

            registration = f"Дата регистрации в боте: <i>{settings[2]}</i>\n"
            days = f"Дней в сервисе: <i>{get_days(settings[2])}</i>\n"
            tasks = f"Выполнено ежедневных заданий: <i>{settings[3]}</i>\n\n"
            dairy_text = f"В дневнике настроения записей пока нет."
            if dairy:
                dairy = dairy[0]
                dairy_text = f"Дневник настроения:\n☺️: {dairy[1]}\n🙂: {dairy[2]}\n😐: {dairy[3]}\n🙁: {dairy[4]}\n😞: {dairy[5]}\n"

            text = ANSWERS["statistics"]["message"] + registration + days + tasks + dairy_text
            inline = make_inline(ANSWERS["statistics"]["inline"], ANSWERS["statistics"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Возвращение в главное меню
    @router_for_callbacks.callback_query(F.data.startswith("*menu*"))
    async def menu_back(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Возвращение в главное меню")

        try:
            inline = make_inline(ANSWERS["menu"]["inline"], ANSWERS["menu"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["menu"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")


def physical_well_being(data: Data):
    # Советы (физическое благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*advices*"))
    async def advices(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Советы")

        try:
            advice = choice(ADVICES)
            await callback_query.answer(text=advice, show_alert=True)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Ежедневные задания (физическое благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*tasks*"))
    async def tasks_back(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Ежеденевные задания")

        try:
            tasks = get_tasks(id_user, data)
            text1 = "1) " + (f"<s>{tasks[2]}</s>" if tasks[1] == 1 else tasks[2]) + "\n"
            text2 = "2) " + (f"<s>{tasks[4]}</s>" if tasks[3] == 1 else tasks[4]) + "\n"
            text3 = "3) " + (f"<s>{tasks[6]}</s>" if tasks[5] == 1 else tasks[6])

            buttons, backend = [], []
            if tasks[1] == 0:
                buttons.append("Выполнить задание №1")
                backend.append("solve1")
            if tasks[3] == 0:
                buttons.append("Выполнить задание №2")
                backend.append("solve2")
            if tasks[5] == 0:
                buttons.append("Выполнить задание №3")
                backend.append("solve3")

            buttons += ANSWERS["tasks"]["inline"]
            backend += ANSWERS["tasks"]["backend"]

            inline = make_inline(buttons, backend, 1, id_user)
            total_text = ANSWERS["tasks"]["message"] + text1 + text2 + text3

            await callback_query.message.edit_text(text=total_text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Возвращение в физическое благополучие
    @router_for_callbacks.callback_query(F.data.startswith("*physical*"))
    async def physical_back(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Вернулся в физическое благополучие")

        try:
            inline = make_inline(ANSWERS["physical"]["inline"], ANSWERS["physical"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["physical"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Выполнение задания
    @router_for_callbacks.callback_query(F.data.startswith("*solve"))
    async def solve(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        task_num = int(str(callback_query.data)[6])
        user_id = color("id=" + str(id_user))
        command = color("Выполнение задания")

        try:
            data.solve_task(id_user, date.today(), task_num)

            tasks = get_tasks(id_user, data)
            text1 = "1) " + (f"<s>{tasks[2]}</s>" if tasks[1] == 1 else tasks[2]) + "\n"
            text2 = "2) " + (f"<s>{tasks[4]}</s>" if tasks[3] == 1 else tasks[4]) + "\n"
            text3 = "3) " + (f"<s>{tasks[6]}</s>" if tasks[5] == 1 else tasks[6])

            buttons, backend = [], []
            if tasks[1] == 0:
                buttons.append("Выполнить задание №1")
                backend.append("solve1")
            if tasks[3] == 0:
                buttons.append("Выполнить задание №2")
                backend.append("solve2")
            if tasks[5] == 0:
                buttons.append("Выполнить задание №3")
                backend.append("solve3")

            buttons += ANSWERS["tasks"]["inline"]
            backend += ANSWERS["tasks"]["backend"]

            inline = make_inline(buttons, backend, 1, id_user)
            total_text = ANSWERS["tasks"]["message"] + text1 + text2 + text3

            await callback_query.message.edit_text(text=total_text, reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")


def social_well_being(data: Data):
    # Советы (социальное благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*advices_social*"))
    async def advices_social(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Советы по социальному благополучию")

        try:
            advice = choice(ADVICES_SOCIAL)
            await callback_query.answer(text=advice, show_alert=True)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Таймер (социальное благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*timer*"))
    async def timer(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Таймер")

        try:
            inline = make_inline(ANSWERS["timer"]["inline"], ANSWERS["timer"]["backend"], 2, id_user)
            await callback_query.message.edit_text(text=ANSWERS["timer"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Социальное благополучие
    @router_for_callbacks.callback_query(F.data.startswith("*social*"))
    async def social_back(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Вернулся в социальное благополучие")

        try:
            inline = make_inline(ANSWERS["social"]["inline"], ANSWERS["social"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["social"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Таймер - засекаем время
    @router_for_callbacks.callback_query(F.data.startswith("*seconds"))
    async def timer_after(callback_query: types.CallbackQuery, state: FSMContext):
        num = int(callback_query.data.split("*")[1][7:])

        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Засекаем время")

        try:
            await callback_query.message.edit_text(text=ANSWERS["timer_after"]["message"], reply_markup=None)
            await state.set_state(Timer.reason)
            await state.update_data(time=num)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Тест (социальное благополучие)
    @router_for_callbacks.callback_query(F.data.startswith("*test*"))
    async def test(callback_query: types.CallbackQuery, state: FSMContext):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Начал проходить тест")

        try:
            await callback_query.message.edit_text(text=ANSWERS["test"]["message1"], reply_markup=None)
            await state.set_state(Test.interests)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Тест - ответил на 3-ий вопрос
    @router_for_callbacks.callback_query(Test.people, F.data.startswith("*answer"))
    async def test3(callback_query: types.CallbackQuery, state: FSMContext):
        id_user = int(callback_query.data.split("*")[2])
        num1, num2 = int(callback_query.data.split("*")[1][6]), int(callback_query.data.split("*")[1][7])
        user_id = color("id=" + str(id_user))
        command = color("Ответил на 3-ий вопрос")

        try:
            text = TEST_DICT[(num1, num2)]
            await state.update_data(people=text)

            await callback_query.message.edit_text(text=ANSWERS["test"]["message4"], reply_markup=None)
            await state.set_state(Test.problems)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")


def psyhological_well_being(data: Data):
    # Возращение в психологическое благополучие
    @router_for_callbacks.callback_query(F.data.startswith("*psyhology*"))
    async def psyhology_back(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Вернулся в психологическое благополучие")

        try:
            inline = make_inline(ANSWERS["psyhology"]["inline"], ANSWERS["psyhology"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["psyhology"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Функция SOS
    @router_for_callbacks.callback_query(F.data.startswith("*sos*"))
    async def sos(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("SOS")

        try:
            inline = make_inline(ANSWERS["sos"]["inline"], ANSWERS["sos"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["sos"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Навигатор помощи
    @router_for_callbacks.callback_query(F.data.startswith("*help*"))
    async def help(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Навигатор помощи")

        try:
            inline = make_inline(ANSWERS["help"]["inline"], ANSWERS["help"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["help"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Буллинг (навигатор помощи)
    @router_for_callbacks.callback_query(F.data.startswith("*bulling*"))
    async def bulling(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Буллинг")

        try:
            inline = make_inline(ANSWERS["bulling"]["inline"], ANSWERS["bulling"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["bulling"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Конфликты с родителями (навигатор помощи)
    @router_for_callbacks.callback_query(F.data.startswith("*conflicts*"))
    async def conflicts(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Конфликты с родителями")

        try:
            inline = make_inline(ANSWERS["conflicts"]["inline"], ANSWERS["conflicts"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["conflicts"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Стресс перед экзаменом (навигатор помощи)
    @router_for_callbacks.callback_query(F.data.startswith("*stress*"))
    async def stress(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Стресс перед экзаменом")

        try:
            inline = make_inline(ANSWERS["stress"]["inline"], ANSWERS["stress"]["backend"], 1, id_user)
            await callback_query.message.edit_text(text=ANSWERS["stress"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Дневник настроения (навигатор помощи)
    @router_for_callbacks.callback_query(F.data.startswith("*dairy*"))
    async def dairy(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        user_id = color("id=" + str(id_user))
        command = color("Дневник настроения")

        try:
            inline = make_inline(ANSWERS["dairy"]["inline"], ANSWERS["dairy"]["backend"], 5, id_user)
            await callback_query.message.edit_text(text=ANSWERS["dairy"]["message"], reply_markup=inline)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")

    # Дневник настроения - выбор эмодзи (навигатор помощи)
    @router_for_callbacks.callback_query(F.data.startswith("*dairy_"))
    async def dairy_update(callback_query: types.CallbackQuery):
        id_user = int(callback_query.data.split("*")[2])
        emotion = callback_query.data.split("*")[1][6:]
        user_id = color("id=" + str(id_user))
        command = color("Дневник настроения - выбор эмодзи")

        try:
            info = data.get_dairy(id_user)
            if info == []:
                value = 1
            else:
                value = 1 + info[0][DAIRY_INDEX[emotion]]
                if info[0][6] == str(date.today()):
                    await callback_query.answer(text=ANSWERS["dairy"]["message_after2"], show_alert=True)
                    return

            data.set_dairy(id_user, date.today(), emotion, value)
            await callback_query.answer(text=ANSWERS["dairy"]["message_after1"], show_alert=True)

            logger.info(f"Пользователь с {user_id} активировал {command}")

        except Exception as e:  # на случай непредвиденной ошибки
            logger.error(f"Пользователь с {user_id} активировал {command}\nОшибка: {e}")
