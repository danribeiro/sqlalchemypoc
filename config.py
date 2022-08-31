from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
USER = config('POSTGRES_USER')
PASSWORD = config('POSTGRES_PASSWORD')
HOST = config('POSTGRES_HOST')
DATABASE = config('POSTGRES_DB')
PORT = config('POSTGRES_PORT')

DATABASE_CONNECTION_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(USER,PASSWORD,HOST,PORT,DATABASE)