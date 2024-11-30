import sqlite3


def connect_or_create_db():
    return sqlite3.connect('user_with_grades.db')


def create_table():
    connect = connect_or_create_db()
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            userid INTEGER PRIMARY KEY AUTOINCREMENT,
            fio VARCHAR(100) NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades(
            gradeid INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER,
            subject VARCHAR(100) NOT NULL,
            grade INTEGER NOT NULL,
            FOREIGN KEY (userid) REFERENCES users(userid)
        )
    ''')

    connect.commit()
    connect.close()


def add_user(fio, age):
    connect = connect_or_create_db()
    cursor = connect.cursor()
    cursor.execute(
        'INSERT INTO users(fio, age) VALUES (?, ?)',
        (fio, age)
    )
    connect.commit()
    connect.close()


def add_grade(userid, subject, grade):
    connect = connect_or_create_db()
    cursor = connect.cursor()
    cursor.execute(
        'INSERT INTO grades(userid, subject, grade) VALUES (?, ?, ?)',
        (userid, subject, grade)
    )
    connect.commit()
    connect.close()


def get_user_with_grades():
    connect = connect_or_create_db()
    cursor = connect.cursor()

    cursor.execute('''
        SELECT users.fio, users.age, grades.subject, grades.grade
        FROM users
        RIGHT JOIN grades ON users.userid = grades.userid
    ''')

    rows = cursor.fetchall()
    for i in rows:
        print(i)

    connect.close()


create_table()

add_user('Ardager', 25)
add_user('Krampoos', 25)
add_user('Anarbekova', 19)


add_grade(1, 'Алгебра', 3)
add_grade(1, 'Русский', 2)
add_grade(2, 'Алгебра', 5)

get_user_with_grades()
