import sqlite3

# Класс, для удобного взаимодействия с БД
class Data:
    # Открытие (или создание) БД
    def __init__(self):  
        self.connection = sqlite3.connect("Bot/data/data.db")
        self.cursor = self.connection.cursor()

        # Таблица для подключения заданий на велосипед и плавание в ежедневные
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Settings (
            USER_ID INTEGER PRIMARY KEY,
            SWIMMING INTEGER NOT NULL,
            BICYCLE INTEGER NOT NULL,
            DATE TEXT NOT NULL,
            TASK_AMOUNT INTEGER NOT NULL)
        """)

        # Таблица ежедневных заданий пользователей
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
            USER_ID INTEGER NOT NULL,
            Task1 INTEGER NOT NULL,
            Text1 TEXT NOT NULL,
            Task2 INTEGER NOT NULL,
            Text2 TEXT NOT NULL,
            Task3 INTEGER NOT NULL,
            Text3 TEXT NOT NULL,
            Data TEXT NOT NULL)
        """)
    
    # Добавление новго пользователя в БД 
    def add_user(self, user_id: int, date: str):
        all_users = self.cursor.execute("SELECT USER_ID FROM Settings").fetchall()

        if (user_id,) not in all_users:
            self.cursor.execute("INSERT INTO Settings (USER_ID, SWIMMING, BICYCLE, DATE, TASK_AMOUNT) VALUES (?, ?, ?, ?, ?)",
                                (user_id, 0, 0, date, 0))
            self.connection.commit()

    # Изменние настроек о добавление плавания/велосипеда в ежедневные задания
    def change_settings(self, user_id: int, type_task: str, value: int):
        self.cursor.execute(f"UPDATE Settings SET {type_task} = ? WHERE USER_ID = ?",
                             (value, user_id))
        self.connection.commit()
    
    # Получение данных об плавании и велосипеда в ежедневных заданиях, а также дату регистрации
    def get_settings(self, user_id: int) -> tuple:
        result = self.cursor.execute("SELECT SWIMMING, BICYCLE, DATE, TASK_AMOUNT FROM Settings WHERE USER_ID = ?", (user_id,)).fetchone()
        return result
    
    # Получение данных об заданиях пользователей на сегодняшний день
    def get_tasks(self, user_id: int, date: str) -> list:
        result = self.cursor.execute("SELECT * FROM Tasks WHERE USER_ID = ? AND Data = ?", (user_id, date)).fetchall()

        return result
    
    # Добавление сгенерированных ежедневных задач польхователя в БД
    def add_tasks(self, user_id: int, date: str, tasks_text: list[str]):
        self.cursor.execute("INSERT INTO Tasks (USER_ID, TASK1, TEXT1, TASK2, TEXT2, TASK3, TEXT3, DATA) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                             (user_id, 0, tasks_text[0], 0, tasks_text[1], 0, tasks_text[2], date))
        self.connection.commit()
    
    # Фиксирование того, что пользователь выполнил задание
    def solve_task(self, user_id: int, date: str, task: int):
        self.cursor.execute(f"""UPDATE Tasks SET Task{task} = ? WHERE USER_ID = ? AND Data = ?""",
                             (1, user_id, date))
        
        settings = self.get_settings(user_id)
        self.cursor.execute(f"""UPDATE Settings SET TASK_AMOUNT = ? WHERE USER_ID = ?""",
                             (settings[3] + 1, user_id))
        self.connection.commit()
    
    def get_all_id(self) -> tuple:
        all_users = self.cursor.execute("SELECT USER_ID FROM Settings").fetchall()

        return all_users