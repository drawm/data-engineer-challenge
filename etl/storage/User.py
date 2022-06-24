from psycopg import Cursor, Connection


class User:
    def __init__(self, conn: Connection, cur: Cursor):
        self.conn = conn
        self.cur = cur

    def get_by_id(self, id: int):
        result = self.cur.execute("""
            select external_id as id, name, address, job, score from users
            where external_id = %s
        """, [id]).fetchall()
        return result

    def insert(self, user):
        print('Inserting user')
        self.cur.execute(
            """
            INSERT INTO
                users (external_id , name , address , job , score)
                VALUES (%s,%s,%s,%s,%s)
            """,
            [user.id, user.name, user.address, user.job, user.score]
        )
        self.conn.commit()
