# coding=utf-8
import sqlite3
from random import randint



def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with sqlite3.connect('blog.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


# функция, которая должна проверять есть переменная в базе или нет
@ensure_connection
def user_id_in_base(conn, user_id: int):
    user_in_base = False
    c = conn.cursor()
    for row in c.execute("SELECT user_id FROM referal"):
        if row[0] == user_id:
            user_in_base = True
            break
        else:
            user_in_base = False
            print(row[0], user_id)
            continue

    return user_in_base

# Добавление записи в базу данных с реф - кошельками пользователей и их уникальными кодами для таблицы рефералов
@ensure_connection
def add_message_to_ref_user_base(conn, user_id: int, wallet: str, curator: str, ref_invited=0):
    c = conn.cursor()
    c.execute('INSERT INTO referal (user_id, wallet, curator, ref_invited) VALUES (?, ?, ?, ?)',
              (user_id, wallet, curator, ref_invited))
    conn.commit()

# функция, которая прибавляет +1 одного пользователя к куратору
@ensure_connection
def add_curator_ref_member(conn, find_user_id: int):
    ref_invited_new = find_ref_curator_of_member(user_id=find_user_id) + 1
    print(ref_invited_new)
    c = conn.cursor()
    sql_update_query = """UPDATE referal SET ref_invited = ? WHERE user_id = ?"""
    data = (ref_invited_new, find_user_id)
    c.execute(sql_update_query, data)
    conn.commit()


# Ретурн найденного человека в базе
@ensure_connection
def get_have_user_in_a_base(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id, ))
    user_result_id = c.fetchall()
    if not user_result_id:
        return 0
    else:
        return 1


# Добавление нового кошелька с нулевым балансом
@ensure_connection
def add_new_wallet_to_base(conn, user_id: int):
    c = conn.cursor()
    c.execute(
        'INSERT INTO wallet (user_id, balance) VALUES (?, ?)',
        (user_id, 0))
    conn.commit()
    print('Store add a new wallet')


# Добавление в общую базу нового юзера
@ensure_connection
def add_new_user_to_base(conn, user_id: int, username: str, date: str):
    c = conn.cursor()
    c.execute(
        'INSERT INTO user (user_id, username, date) VALUES (?, ?, ?)',
        (user_id, username, date))
    conn.commit()
    print('Store have a new user')


# Ретурн всех категорий магазина
@ensure_connection
def get_full_list_categories_of_store(conn, ):
    store_categories = []
    c = conn.cursor()
    for row in c.execute("SELECT title FROM category"):
        store_categories.append(row[0])

    return store_categories


# Ретурн всех подкатегорий магазина
@ensure_connection
def get_full_list_podcategories_of_store(conn, ):
    store_categories = []
    c = conn.cursor()
    for row in c.execute("SELECT title FROM pod_category"):
        store_categories.append(row[0])

    return store_categories

# Ретурн баланса определённого пользователя
@ensure_connection
def get_balance_of_user(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT balance FROM wallet WHERE user_id = ?", (user_id, ))
    user_balance = c.fetchall()
    return user_balance[0][0]


# функция, которая находит кол - во рефералов в данный момент у куратора
@ensure_connection
def find_ref_curator_of_member(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT * FROM referal WHERE user_id = ?", (user_id,))
    explore_list = c.fetchall()
    for row in explore_list:
        return int(row[4])


# функция, которая находит название товара по заданной категории
@ensure_connection
def get_name_tovara_po_podcategory(conn, name_category: str):
    name_tovara = []
    c = conn.cursor()
    for row in c.execute("SELECT title FROM product WHERE category = ?", (name_category, )):
        name_tovara.append(row[0])

    return name_tovara 


# функция, которая возвращает название всех подкатегорий по категориям
@ensure_connection
def get_name_podcategory_po_category(conn, name_category: str):
    name_podcategory = []
    c = conn.cursor()
    for row in c.execute("SELECT title FROM pod_category WHERE main_category = ?", (name_category, )):
        name_podcategory.append(row[0])

    return name_podcategory

# Ретурн всех товаров магазина
@ensure_connection
def get_full_name_products_of_store(conn, ):
    store_products = []
    c = conn.cursor()
    for row in c.execute("SELECT title FROM product"):
        store_products.append(row[0])

    return store_products


# Ретурн по названию товара его цену 
@ensure_connection
def get_name_tovara_price(conn, name_tovara: str):
    c = conn.cursor()
    c.execute("SELECT price FROM product WHERE title = ?", (name_tovara, ))
    tovar_info = c.fetchall()
    return tovar_info[0][0]


# Ретурн по названию товара его количество
@ensure_connection
def get_name_tovara_kolvo(conn, name_tovara: str):
    c = conn.cursor()
    c.execute("SELECT kolvo FROM product WHERE title = ?", (name_tovara, ))
    tovar_info = c.fetchall()
    return tovar_info[0][0]


# Ретурн по названию товара его описание
@ensure_connection
def get_name_tovara_description(conn, name_tovara: str):
    c = conn.cursor()
    c.execute("SELECT description FROM product WHERE title = ?", (name_tovara, ))
    tovar_info = c.fetchall()
    return tovar_info[0][0]


# Ретурн баланса определённого пользователя
@ensure_connection
def get_balance_of_user(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT balance FROM wallet WHERE user_id = ?", (user_id, ))
    user_balance = c.fetchall()
    return user_balance[0][0]


# Изменение баланса определённого пользователя
@ensure_connection
def update_balance_of_user(conn, balance: int, user_id: int):
    c1 = conn.cursor()
    sql_update_query = """UPDATE wallet SET balance = ? WHERE user_id = ?"""
    data = (balance, user_id)
    c1.execute(sql_update_query, data)
    conn.commit()
    print('Me update a balance of player')


# Ретурн по названию товара его цену 
@ensure_connection
def get_name_tovara_price(conn, name_tovara: str):
    c = conn.cursor()
    c.execute("SELECT price FROM product WHERE title = ?", (name_tovara, ))
    tovar_info = c.fetchall()
    return tovar_info[0][0]



# Изменение количества определённого товара
@ensure_connection
def update_kolvo_of_product(conn, kolvo_tovara: int, name_tovara: str):
    c1 = conn.cursor()
    sql_update_query = """UPDATE product SET kolvo = ? WHERE title = ?"""
    data = (kolvo_tovara, name_tovara)
    c1.execute(sql_update_query, data)
    conn.commit()
    print('Me update a kolvo tovara')


# Изменение количества товара по его названию
@ensure_connection
def get_name_tovara_kolvo(conn, name_tovara: str):
    c = conn.cursor()
    c.execute("SELECT kolvo FROM product WHERE title = ?", (name_tovara, ))
    tovar_info = c.fetchall()
    return tovar_info[0][0]


# Добавление покупки в список покупок пользователя
@ensure_connection
def add_sale_to_sells_base(conn, user_id: int, name_tovara: str, kolvo_tovara: str, data_of_sale: str, time_of_sale: str):
    c = conn.cursor()
    c.execute('INSERT INTO sales (id_user, name_tovara, kolvo_tovara, data_of_sale, time_of_sale) VALUES (?, ?, ?, ?, ?)',
              (user_id, name_tovara, kolvo_tovara, data_of_sale, time_of_sale))
    conn.commit()


# Вывод текста акканута, который купил пользователь
@ensure_connection
def get_text_from_account_base(conn, product_name: str):
    c = conn.cursor()
    c.execute("SELECT account_text FROM account WHERE product_name = ?", (product_name, ))
    tovar_info = c.fetchone()
    return tovar_info[0]

# Ввод данных о текущей покупке
@ensure_connection
def in_text_real_sale(conn, user_id: int, item_name: str, count: int):
    c = conn.cursor()
    c.execute('INSERT INTO realsale (user_id, item_name, count) VALUES (?, ?, ?)',
              (user_id, item_name, count))
    conn.commit()

# Вывод названия товара из риалтайм покупки пользователя
@ensure_connection
def get_item_name_from_real_sale(conn, user_id: int):
    c = conn.cursor()
    c.execute("SELECT item_name FROM realsale WHERE user_id = ?", (user_id, ))
    return_name = c.fetchall()
    return return_name[0][0]

# Вывод названия изображения из категории
@ensure_connection
def get_filename_of_category_image(conn, title: int):
    c = conn.cursor()
    c.execute("SELECT image FROM category WHERE title = ?", (title, ))
    return_name = c.fetchall()
    return return_name[0][0]

# Вывод названия изображения из подкатегории
@ensure_connection
def get_filename_of_podcategory_image(conn, title: int):
    c = conn.cursor()
    c.execute("SELECT image FROM pod_category WHERE title = ?", (title, ))
    return_name = c.fetchall()
    return return_name[0][0]

# Функция, которая удаляет все риал - сейлы клиента, чтобы записать новый
@ensure_connection
def delete_realsales_user_id(conn, user_id: int):
    c = conn.cursor()
    c.execute("DELETE FROM realsale WHERE user_id = ?", (user_id, ))
    conn.commit()

# Функция, которая выводит все названия кнопок, которые добавлены в боте
@ensure_connection
def get_names_of_buttons_main_menu(conn, ):
    button_names = []
    c = conn.cursor()
    for row in c.execute("SELECT name FROM tel_button"):
        button_names.append(row[0])

    return button_names


# Функция вывода из базы данных текста, который прикреплен к кнопке
@ensure_connection
def get_text_of_button_id(conn, id: int):
    c = conn.cursor()
    c.execute("SELECT text FROM tel_button WHERE id = ?", (id, ))
    return_name = c.fetchall()
    return return_name[0][0]


if __name__ == "__main__":
    print(get_text_of_button_id(id=1))


