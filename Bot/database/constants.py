import json
import os
from dotenv import load_dotenv

# Загружаем данные из .env 
load_dotenv("Bot/data/.env")
API_TOKEN = os.getenv("API_KEY")

# Загрзука готовых ответов
with open("Bot/data/answers.json", encoding="utf-8") as json_file:
    ANSWERS = json.load(json_file)

# Загрзука интенсива
with open("Bot/data/intensive.json", encoding="utf-8") as json_file:
    INTENSIVE = json.load(json_file)

# Загрзука заданий
with open("Bot/data/tasks.json", encoding="utf-8") as json_file:
    TASKS = json.load(json_file)

# Загрзука солветов
with open("Bot/data/advices.json", encoding="utf-8") as json_file:
    ADVICES = json.load(json_file)
