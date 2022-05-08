import os
import sqlite3
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from loader_saver import PostgresSaver, SQLiteLoader
from psycopg2.extensions import connection as _connection

load_dotenv()

# пачка размера 500
size = 500


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, size)
    sqlite_loader = SQLiteLoader(connection, size)

    data = sqlite_loader.load_data()
    postgres_saver.save_all_data(data)


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


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST', '127.0.0.1'),
           'port': os.environ.get('DB_PORT')}

    with conn_context_sqlight('db.sqlite') as sqlite_conn, \
            conn_context_postgres(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
