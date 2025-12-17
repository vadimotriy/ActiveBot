import sqlite3

# Класс, для удобного взаимодействия с БД
class Data:
    # Открытие (или создание) БД
    def __init__(self):  
        self.connection = sqlite3.connect("Bot/data/data.db")
        self.cursor = self.connection.cursor()

        