from peewee import *
from fastapi import FastAPI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str = ''
    db_user: str = ''
    db_password: str = ''


settings = Settings()
db = PostgresqlDatabase(settings.db_name, user=settings.db_user,
                        password=settings.db_password)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(db_column='username')

    class Meta:
        db_table = "users"


class Type(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()

    class Meta:
        db_table = "types"


class Document(BaseModel):
    id = AutoField(primary_key=True)
    uploaderId = ForeignKeyField(User, to_field='id', db_column='uploaderId', backref="user")
    name = TextField()
    uploadDate = DateField()
    creationDate = DateField()
    typeId = ForeignKeyField(Type, to_field='id', db_column='typeId')

    class Meta:
        db_table = "documents"


class Tag(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField()
    autoTag = BooleanField()

    class Meta:
        db_table = "tags"


class DocumentTags(BaseModel):
    tagId = ForeignKeyField(Tag, to_field='id', db_column='tagId')
    documentId = ForeignKeyField(Document, to_field='id', db_column='documentId')
