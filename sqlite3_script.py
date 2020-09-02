# coding=utf-8
import sqlite3

def ensure_connection(func):
    """ Декоратор для подключения к СУБД ( обновляемой - blog.db ): открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with sqlite3.connect('blog.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner

def ensure_connection_new(func):
    """ Декоратор для подключения к СУБД ( обновляемой - blog.db ): открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with sqlite3.connect('db_from_server.db') as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner