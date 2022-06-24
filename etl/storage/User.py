from psycopg import Cursor, Connection

from etl.entities import User


class UserStorage:
    def __init__(self, conn: Connection, cur: Cursor):
        self.conn = conn
        self.cur = cur

    def setup(self):
        print('Setup users table if not exists')
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                external_id INT NOT NULL unique,
                name char(255) NOT NULL,
                address TEXT NOT NULL,
                job char(255) NOT NULL,
                score real NOT NULL,
                last_json_metadata text not null
            );
            CREATE INDEX IF NOT EXISTS external_id ON users (id, external_id);
        """)
        self.conn.commit()

    def get_by_id(self, id: int):
        result = self.cur.execute("""
            select external_id as id, name, address, job, score, last_json_metadata
            from users
            where external_id = %s
        """, [id]).fetchone()

        if result:
            return
        return result

    def insert(self, user: User):
        print('Inserting user')
        self.cur.execute(
            """
            INSERT INTO
                users (external_id , name , address , job , score, last_json_metadata)
                VALUES (%s,%s,%s,%s,%s,%s)
            """,
            [user.id, user.name, user.address, user.job, user.score, user.json_metadata]
        )
        self.conn.commit()
