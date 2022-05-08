import logging
import sqlite3
from dataclasses import asdict, astuple

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
            key: self.__generator(key, val) for key, val in MAP.items()
        }

    def __generator(self, table: str, cls):
        try:
            curs = self.conn.cursor()
            query = f'SELECT * FROM {table};'
            curs.execute(query)
            while True:
                data = curs.fetchmany(self.size)

                list_data = [cls(*i) for i in data]
                if not data:
                    break
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

    def truncate(self, table):
        self.cursor.execute(f"TRUNCATE {table} CASCADE;")

    def save_all_data(self, data_dict: dict):
        for table, data_gen in data_dict.items():
            self.truncate(table)
            counter = 0
            for list_data in data_gen:

                dict_cls = asdict(list_data[0])
                keys_sql = ', '.join(dict_cls.keys())
                count_s = ('%s, ' * len(dict_cls.keys()))[:-2]
                query = (f'INSERT INTO {table} ({keys_sql}) VALUES ({count_s}) '
                         f' ON CONFLICT (id) DO NOTHING;')
                tuple_butch = (astuple(dicts) for dicts in list_data)
                try:
                    self.cursor.executemany(query, tuple_butch)
                except(Exception):
                    logger.error('Error of downloading data in table %s', table)
                counter += len(dict_cls)
            logger.info('Data in table %s is downloaded, count of rows %s', table, counter)

        self.connect.commit()
        self.cursor.close()


MAP = {
    'film_work': Filmwork,
    'person': Person,
    'genre': Genre,
    'genre_film_work': FilmworkGenre,
    'person_film_work': FilmworkPerson,
}
