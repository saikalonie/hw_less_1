# CRUD - Create, Read, Update, Delete

import sqlite3

connect = sqlite3.connect('users.db')
cursor = connect.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        fio VARCHAR (100) NOT NULL,
        age INTEGER NOT NULL,
        hobby TEXT
    )
''')
connect.commit()

def add_user(fio, age, hobby):
    cursor.execute(
        'INSERT INTO users(fio, age, hobby) VALUES (?,?,?)',
        (fio, age, hobby))
    connect.commit()
    print(f"Пользователь {fio} добавлен")


# add_user("Вася Пупкин", 33, "плавание")


def get_all_users():
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    if users:
        # print(users)
        print("Список всех пользователей:")
        for user in users:
            print(f"ФИО: {user[0]}, возраст: {user[1]}, хобби: {user[2]}")
    else:
        print("Список пользователей пуст.")


# get_all_users()


def update_user(fio=None, age=None, hobby=None, rowid=None ):
    if fio:
        cursor.execute(
            'UPDATE users SET fio = ? WHERE rowid = ?',
            (fio, rowid))
        connect.commit()
    if age:
        cursor.execute(
            'UPDATE users SET age = ? WHERE rowid = ?',
            (age, rowid))
        connect.commit()
    if hobby:
        cursor.execute(
            'UPDATE users SET hobby = ? WHERE rowid = ?',
            (hobby, rowid))
        connect.commit()


# update_user(fio="Олег", hobby="Игры", rowid=3)
# get_all_users()

def delete_user(fio):
    cursor.execute(
        'DELETE FROM users WHERE fio = ?',
        (fio,))
    connect.commit()
    print("Пользователь удален")

delete_user(fio="Арзыбек")

connect.close()
