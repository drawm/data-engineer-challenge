class Config:
    def __init__(self, env):
        self.DIR_LOCATION = env.get('EVENT_DIR')
        if self.DIR_LOCATION is None:
            self.DIR_LOCATION = '/app/events/'

        self.POSTGRES_USER = env.get('POSTGRES_USER')
        if self.POSTGRES_USER is None:
            self.POSTGRES_USER='dwh'

        self.POSTGRES_PASSWORD = env.get('POSTGRES_PASSWORD')
        if self.POSTGRES_PASSWORD is None:
            self.POSTGRES_PASSWORD='dwh'

        self.POSTGRES_DB = env.get('POSTGRES_DB')
        if self.POSTGRES_DB is None:
            self.POSTGRES_DB='dwh'

        self.DB_HOST = env.get('DB_HOST')
        if self.DB_HOST is None:
            self.DB_HOST='localhost'

        self.DB_PORT = env.get('DB_PORT')

        if self.DB_PORT is None:
            self.DB_PORT=5432

