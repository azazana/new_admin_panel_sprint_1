import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv

path = '../../03_sqlite_to_postgres'


load_dotenv()

dsl = {'dbname': os.environ.get('DB_NAME'),
       'user': os.environ.get('DB_USER'),
       'password': os.environ.get('DB_PASSWORD'),
       'host': os.environ.get('DB_HOST', '127.0.0.1'),
       'port': os.environ.get('DB_PORT')}

MAP = [
    'film_work',
    'person',
    'genre',
    'genre_film_work',
    'person_film_work',
]


@contextmanager
def conn_context_sqlight(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    # С конструкцией yield вы познакомитесь в следующем модуле
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    conn.close()


@contextmanager
def conn_context_postgres(db_conf):
    conn = psycopg2.connect(**db_conf)
    # conn.row_factory = psycopg2.Row
    yield conn
    # С конструкцией yield вы познакомитесь в следующем модуле
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    conn.close()


def fields(cursor):
    """ Given a DB API 2.0 cursor object that has been executed, returns
    a dictionary that maps each field name to a column index; 0 and up. """
    results = {}
    column = 0
    for d in cursor.description:
        results[d[0]] = column
        column = column + 1

    return results


with conn_context_sqlight(path + '/db.sqlite') as sqlite_conn, \
        conn_context_postgres(dsl) as pg_conn:
    cursor_light = sqlite_conn.cursor()
    cursor_psql = pg_conn.cursor()
    for table in MAP:
        cursor_light.execute(f'Select * from {table};')
        data_light = cursor_light.fetchall()
        cursor_psql.execute(f'Select * from content.{table};')
        data_psql = cursor_psql.fetchall()
        assert len(data_psql) == len(data_light), 'not equal amount of lines'
        index = 0

        colum_names = [desc[0] for desc in cursor_light.description]

        row_light: sqlite3.Row = data_light[0]
        row_psql = data_psql[0]
        field_map = fields(cursor_psql)

        for key_light in row_light.keys():
            assert isinstance(row_light[key_light], type(row_psql[field_map[key_light]])), \
                f'not equal type of data in columns in table {table}' \
                f' columns {key_light} value sqlite {row_light[key_light]}, ' \
                f'type {type(row_light[key_light])}' \
                f' value psql {row_psql[field_map[key_light]]}, ' \
                f'type  {type(row_psql[field_map[key_light]])} '
