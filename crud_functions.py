import sqlite3


def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT ,
    price INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()

    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    )
    ''')
    connection.commit()
    connection.close()


def database_filler(title_product, descr_product=' ', price_product=0):
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    check_product = cursor.execute("SELECT * FROM Products WHERE title= ?", (title_product,))
    if check_product.fetchone() is None:
        cursor.execute('INSERT INTO Products (title,description,price ) VALUES(?, ?, ?)',
                       (f'{title_product}', f'{descr_product}', f'{price_product}')
                       )
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result

def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username= ?", (username,))
    user_included = check_user.fetchone()
    connection.commit()
    connection.close()
    if user_included is None:
        return False
    else:
        return True

def add_user(username, email, age):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username= ?", (username,))
    res = len(check_user.fetchall())
    if res == 0:
        cursor.execute('INSERT INTO Users (username,email,age, balance ) VALUES(?, ?, ?, ?)',
                       (f'{username}', f'{email}', f'{age}', 1000))
    connection.commit()
    connection.close()


initiate_db()

for i in range(1, 5):
    database_filler(f'Product {i}', f'Описание {i}', i * 100)