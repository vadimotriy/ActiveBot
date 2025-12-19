import json
import os
from dotenv import load_dotenv

# Загружаем данные из .env 
load_dotenv("Bot/data/.env")
API_TOKEN = os.getenv("API_KEY")

# Загрзука готовых ответов
with open("Bot/data/answers.json", encoding="utf-8") as json_file:
    ANSWERS = json.load(json_file)

# Загрзука заданий
with open("Bot/data/tasks.json", encoding="utf-8") as json_file:
    TASKS = json.load(json_file)

# Загрзука советов по физическому благополучию
with open("Bot/data/advices.json", encoding="utf-8") as json_file:
    ADVICES = json.load(json_file)

# Загрзук советов по социальному благополучию
with open("Bot/data/advices_social.json", encoding="utf-8") as json_file:
    ADVICES_SOCIAL = json.load(json_file)


from aiogram.fsm.state import StatesGroup, State

# State, для того чтобы пользователь мог ответить нам
class Timer(StatesGroup):
    reason = State()