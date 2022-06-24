import json

from psycopg import Cursor, Connection

from entities.Card import Card


def tuple_to_entity(result) -> Card:
    (id, user_id, created_by_name, updated_at, created_at, active, last_json_metadata) = result
    return Card(
        {
            "id": id,
            "user_id": user_id,
            "created_by_name": created_by_name,
            "updated_at": updated_at,
            "created_at": created_at,
            "active": active
        },
        json.loads(last_json_metadata)
    )


class CardStorage:
    def __init__(self, conn: Connection, cur: Cursor):
        self.conn = conn
        self.cur = cur

    def setup(self):
        print('Setup cards table if not exists')
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS cards (
                id SERIAL PRIMARY KEY,
                external_id INT NOT NULL unique,
                user_id INT NOT NULL,
                created_by_name char(255) NOT NULL,
                updated_at char(255) NOT NULL,
                created_at char(255) NOT NULL,
                active bool default false,
                last_json_metadata text not null
            );
            CREATE INDEX IF NOT EXISTS external_id ON cards (id, external_id);
        """)
        self.conn.commit()

    def get_by_id(self, id: int) -> Card:
        result = self.cur.execute("""
            select external_id as id, user_id, created_by_name, updated_at, created_at, active, last_json_metadata
            from cards
            where external_id = %s
        """, [id]).fetchone()

        if not result:
            return None

        return tuple_to_entity(result)

    def insert(self, card: Card):
        print('Inserting card')
        self.cur.execute(
            """
            INSERT INTO
                cards (external_id, user_id, created_by_name, updated_at, created_at, active, last_json_metadata)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            [card.id, card.user_id, card.created_by_name, card.updated_at, card.created_at, card.active,
             card.json_metadata]
        )
        self.conn.commit()

    def update(self, card: Card):
        print('Updating card')
        self.cur.execute(
            """
            UPDATE cards
            SET external_id = %s,   
                user_id = %s,
                created_by_name = %s,
                updated_at = %s,
                created_at = %s,
                active = %s,
                last_json_metadata = %s
            WHERE external_id = %s
            """,
            [card.id, card.user_id, card.created_by_name, card.updated_at, card.created_at, card.active,
             card.json_metadata, card.id]
        )
        self.conn.commit()
