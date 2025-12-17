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
            BICYCLE INTEGER NOT NULL)
        """)

        # Таблица ежедневных заданий пользователей
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tasks (
            USER_ID INTEGER PRIMARY KEY,
            Task1 INTEGER NOT NULL,
            Text1 TEXT NOT NULL,
            Task2 INTEGER NOT NULL,
            Text2 TEXT NOT NULL,
            Task3 INTEGER NOT NULL,
            Text3 TEXT NOT NULL,
            Data TEXT NOT NULL)
        """)
    
    # Добавление новго пользователя в БД 
    def add_user(self, user_id: int):
        all_users = self.cursor.execute('SELECT USER_ID FROM Settings').fetchall()
        print(all_users)

        if (user_id,) not in all_users:
            self.cursor.execute('INSERT INTO Settings (USER_ID, SWIMMING, BICYCLE) VALUES (?, ?, ?)',
                                (user_id, 0, 0))
            self.connection.commit()

    # Изменние настроек о добавление плавания/велосипеда в ежедневные задания
    def change_settings(self, user_id: int, type_task: str, value: int):
        self.cursor.execute(f"""UPDATE Settings SET {type_task} = ? WHERE USER_ID = ?""",
                             (value, user_id))
        self.connection.commit()
    
    # Получение данных об плавании и велосипеда в ежедневных заданиях
    def get_settings(self, user_id: int) -> tuple[int]:
        result = self.cursor.execute('SELECT SWIMMING, BICYCLE FROM Settings '
                                      'WHERE USER_ID = ?', (user_id,)).fetchone()
        return result