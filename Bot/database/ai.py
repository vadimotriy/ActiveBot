import aiohttp
import json
import asyncio

from Bot.database.constants import BASE_PROMT

# асинхронная функция для запроса к API
async def openrouter_request(prompt: str, api_key: str):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "qwen/qwen3-235b-a22b:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(payload)) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_text = await response.text()
                raise Exception(f"OpenRouter error {response.status}: {error_text}")

# Функция для получения промта для профориентационного теста
def get_promt(interests: str, subjects: str, people: str, problems: str) -> str:
    text = BASE_PROMT
    text += f"Интересы пользователя: {interests}\n"
    text += f"Школьные и вузовские предметы, которые интересует пользователя: {subjects}\n"
    text += f"{people}\n"
    text += f"Ограничения пользователя по здоровью: {problems}\n"

    return text