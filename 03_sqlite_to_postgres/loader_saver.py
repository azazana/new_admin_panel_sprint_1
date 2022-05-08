import sqlite3
from dataclasses import asdict, astuple

from data_classes import Filmwork, FilmworkGenre, FilmworkPerson, Genre, Person


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
        curs = self.conn.cursor()
        query = f'SELECT * FROM {table};'
        curs.execute(query)
        # try:
        while True:
            data = curs.fetchmany(self.size)

            list_data = [cls(*i) for i in data]
            if not data:
                break
            yield list_data

        # except Exception:
            # logger
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
            # self.truncate(table)
            for list_data in data_gen:
                dict_cls = asdict(list_data[0])
                keys_sql = ', '.join(dict_cls.keys())
                count_s = ('%s, ' * len(dict_cls.keys()))[:-2]
                query = (f'INSERT INTO {table} ({keys_sql}) VALUES ({count_s}) '
                         f' ON CONFLICT (id) DO NOTHING;')
                tupple_butch = (astuple(dicts) for dicts in list_data)
                self.cursor.executemany(query, tupple_butch)

        self.connect.commit()
        self.cursor.close()

#
# def from_dict_to_dataclass(cls, data):
#     return cls(
#         **{
#             key: (data[key] if val.default == val.empty else data.get(key, val.default))
#             for key, val in inspect.signature(Filmwork).parameters.items()
#         }
#     )


MAP = {
    'film_work': Filmwork,
    'person': Person,
    'genre': Genre,
    'genre_film_work': FilmworkGenre,
    'person_film_work': FilmworkPerson,
}

#
# connection = psycopg2.connect(
#     host=os.environ.get('DB_HOST', '127.0.0.1'),
#     database=os.environ.get('DB_NAME'),
#     user=os.environ.get('DB_USER'),
#     password=os.environ.get('DB_PASSWORD'),
#     port=os.environ.get('DB_PORT')
# )
# connection.autocommit = True
