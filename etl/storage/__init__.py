import psycopg
import os

from psycopg import Cursor, Connection

from etl.config import Config
from etl.storage.User import User

config = Config(os.environ)

# Will be decoupled and made to support more event type later
def db_setup(conn, cur):
    print('Setup database table if not exists')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            external_id INT NOT NULL,
            name char(255) NOT NULL,
            address TEXT NOT NULL,
            job char(255) NOT NULL,
            score real NOT NULL
        );
        CREATE INDEX IF NOT EXISTS external_id ON users (id, external_id);
    """)
    conn.commit()


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

    cur = conn.cursor()
    return (conn, cur)

class Storage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating storage access instance')

            cls._instance = super(Storage, cls).__new__(cls)

            (conn, cur) = connect()
            db_setup(conn, cur)
            cls._instance.user = User(conn, cur)
            cls._instance.conn = conn
            cls._instance.cur = cur

            # Put any initialization here.
        return cls._instance
