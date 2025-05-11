from peewee import (
    AutoField,
    BooleanField,
    CharField,
    CompositeKey,
    DateField,
    ForeignKeyField,
    Model,
)

from app.db import db


class BaseModel(Model):
    class Meta:
        database = db


class UserModel(BaseModel):
    id = AutoField()
    name = CharField(db_column="username")

    class Meta:
        db_table = "users"


class DocumentTypeModel(BaseModel):
    id = AutoField()
    name = CharField(unique=True)

    class Meta:
        db_table = "types"


class DocumentModel(BaseModel):
    id = AutoField()
    uploader = ForeignKeyField(UserModel, backref="documents")
    name = CharField(max_length=255)
    upload_date = DateField()
    creation_date = DateField()
    type = ForeignKeyField(DocumentTypeModel, backref="documents")

    class Meta:
        db_table = "documents"


class TagModel(BaseModel):
    id = AutoField()
    name = CharField(unique=True)
    auto_tag = BooleanField()

    class Meta:
        db_table = "tags"


class DocumentTagModel(BaseModel):
    document = ForeignKeyField(DocumentModel)
    tag = ForeignKeyField(TagModel)

    class Meta:
        primary_key = CompositeKey("document", "tag")
        db_table = "document_tags"


def create_tables():
    db.create_tables(
        [
            UserModel,
            DocumentTypeModel,
            DocumentModel,
            TagModel,
            DocumentTagModel,
        ]
    )
