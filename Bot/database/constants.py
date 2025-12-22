import json
import os
from dotenv import load_dotenv

# Загружаем данные из .env 
load_dotenv("Bot/data/.env")
API_TOKEN = os.getenv("API_KEY")
API_OPEN_ROUTER = os.getenv("API_OPEN_ROUTER")
ADMIN = os.getenv("ADMIN")

# Загрузка готовых ответов
with open("Bot/data/answers.json", encoding="utf-8") as json_file:
    ANSWERS = json.load(json_file)

    # Основа для промта
    BASE_PROMT = ANSWERS["promt"]

# Загрузка заданий
with open("Bot/data/tasks.json", encoding="utf-8") as json_file:
    TASKS = json.load(json_file)

# Загрузка советов по физическому благополучию
with open("Bot/data/advices.json", encoding="utf-8") as json_file:
    ADVICES = json.load(json_file)

# Загрузка советов по социальному благополучию
with open("Bot/data/advices_social.json", encoding="utf-8") as json_file:
    ADVICES_SOCIAL = json.load(json_file)



from aiogram.fsm.state import StatesGroup, State

# State, для того чтобы пользователь мог ответить нам
class Timer(StatesGroup):
    reason = State()

class Test(StatesGroup):
    interests = State()
    subjects = State()
    people = State()
    problems = State()


TEST_DICT = {
    (0, 0): "Пользователь не умеет работать с людьми и не хочет.",
    (0, 1): "Пользователь не умеет работать с людьми, но хочет.",
    (1, 0): "Пользователь умеет работать с людьми, но не хочет.",
    (1, 1): "Пользователь умеет работать с людьми и хочет.",
    (2, 2): "Пользователь еще не определился - хочет ли он работать с людьми."
}

DAIRY_INDEX = {
    "very_happy": 1,
    "happy": 2,
    "normal": 3,
    "sad": 4,
    "very_sad": 5
}

