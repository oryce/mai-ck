from peewee import DatabaseProxy
from playhouse.db_url import connect

from app.config import Settings

db = DatabaseProxy()


def init_db():
    global db

    settings = Settings()

    real_db = connect(str(settings.pg_dsn))

    db.initialize(real_db)
    db.connect(reuse_if_open=True)
