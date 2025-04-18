from peewee import Database
from playhouse.db_url import connect

from app.config import Settings

db: Database


def init_db():
    global db

    settings = Settings()
    db = connect(str(settings.pg_dsn))
    db.connect(reuse_if_open=True)
