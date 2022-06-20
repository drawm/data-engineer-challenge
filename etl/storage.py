import os

from psycopg import Connection, Cursor

from config import Config
import json
import psycopg

print("Starting ETL")

print("Extracting configuration")
config = Config(os.environ)


def load_json_file(path):
    io_handle = open(path, "r")
    json_data = json.load(io_handle)
    io_handle.close()
    return json_data


# Will be decoupled and made to support more event type later
def insert_event(cursor, event):
    print(event)
    cursor.execute(
        """
            INSERT INTO users(external_id, name, address, job, score)
            VALUES (%(id)s, %(name)s, %(address)s, %(job)s, %(score)s)
        """,
        event['payload']
    )


# Will be decoupled and made to support more event type later
def db_setup() -> str:
    return """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            external_id INT NOT NULL,
            name char(255) NOT NULL,
            address TEXT NOT NULL,
            job char(255) NOT NULL,
            score real NOT NULL
        )
    """


def connect() -> (Cursor, Connection):
    conn = psycopg.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        host=config.DB_HOST,
        port=config.DB_PORT,
        password=config.POSTGRES_PASSWORD
    )
    print('DB connection successful')

    print('Setup database table if not exists')
    cur = conn.cursor()
    return (cur, conn)

class UserStorage:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur

    def get_by_id(self, id:int):
        result = self.cur.execute("""
            select * from users
            where external_id = %s
        """, id)
        print(result)
        return result

class Storage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Storage, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self):
        (cur, conn) = connect()

        cur.execute(db_setup())
        conn.commit()

        self.user = UserStorage()

