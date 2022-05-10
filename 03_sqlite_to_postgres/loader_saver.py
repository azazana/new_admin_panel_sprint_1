import logging
import sqlite3
from dataclasses import asdict, astuple

import psycopg2.extras as psql
from data_classes import Filmwork, FilmworkGenre, FilmworkPerson, Genre, Person

logging.basicConfig(filename='logging.log', level=logging.INFO,
                    format='%(asctime)s  %(message)s')

logger = logging.getLogger(__name__)


class SQLiteLoader:

    def __init__(self, conn: sqlite3.Connection, size: int):
        conn.row_factory = sqlite3.Row
        self.conn = conn
        self.size = size

    def load_data(self):
        return {
            key: self.__generator(key, val) for key, val in MappingTable_DataClass.items()
        }
        self.conn.close()

    def __generator(self, table: str, model):
        try:
            curs = self.conn.cursor()
            query = f'SELECT * FROM {table};'
            curs.execute(query)
            while data := curs.fetchmany(self.size):
                list_data = [model(*i) for i in data]
                yield list_data

            logger.info('Reading data from table %s is succeed', table)
        except sqlite3.DatabaseError as err:
            logger.error('Error of reading sqlite in table %s \n %s', table, err)
            # pass


class PostgresSaver:

    def __init__(self, connect, size):
        self.connect = connect
        self.size = size
        self.cursor = self.connect.cursor()

    # def truncate(self, table):
    #     self.cursor.execute(f"TRUNCATE {table} CASCADE;")

    def save_all_data(self, data_dict: dict):
        for table, data_gen in data_dict.items():
            # self.truncate(table)
            counter = 0
            for list_data in data_gen:

                dict_cls = asdict(list_data[0])
                keys_sql = ', '.join(dict_cls.keys())
                set_keys = ', '.join([f'{i} = EXCLUDED.{i}' for i in dict_cls.keys()])
                count_s = ', '.join(['%s'] * len(dict_cls))
                query = (f'INSERT INTO {table} ({keys_sql}) VALUES ({count_s}) '
                         f' ON CONFLICT (id) DO UPDATE'
                         f' SET {set_keys};')
                tuple_butch = [astuple(dicts) for dicts in list_data]
                try:
                    psql.execute_batch(self.cursor, query, tuple_butch)
                except(Exception) as err:
                    logger.error('Error of downloading data in table %s. Error %s', table, err)
                counter += len(list_data)
            logger.info('Data in table %s is downloaded, count of rows %s', table, counter)
        self.cursor.close()
        self.connect.commit()
        self.connect.close()


MappingTable_DataClass = {
    'film_work': Filmwork,
    'person': Person,
    'genre': Genre,
    'genre_film_work': FilmworkGenre,
    'person_film_work': FilmworkPerson,
}
