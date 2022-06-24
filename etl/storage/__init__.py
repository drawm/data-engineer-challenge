import psycopg
import os

from psycopg import Cursor, Connection

from config import Config
from storage.Card import CardStorage
from storage.User import UserStorage

config = Config(os.environ)


def connect() -> (Connection, Cursor):
    print('Connecting to db')
    conn = psycopg.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        host=config.DB_HOST,
        port=config.DB_PORT,
        password=config.POSTGRES_PASSWORD
    )
    print('DB connection successful')

    return conn, conn.cursor()


class Storage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating storage access instance')

            cls._instance = super(Storage, cls).__new__(cls)

            # Initialization goes here
            (conn, cur) = connect()
            cls._instance.conn = conn
            cls._instance.cur = cur

            cls._instance.user = UserStorage(conn, cur)
            cls._instance.user.setup()

            cls._instance.card = CardStorage(conn, cur)
            cls._instance.card.setup()

        return cls._instance
