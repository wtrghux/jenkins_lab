import os
import main
from peewee import *


DB_NAME = "Database.db"
db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = db


class Clients(BaseModel):
    name = CharField()
    city = CharField()
    address = CharField()


class Orders(BaseModel):
    client = ForeignKeyField(Clients)
    date = DateField()
    amount = CharField()
    description = CharField()


def check_db_exists():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    main.init()
    if os.path.exists(DB_NAME):
        main.fill()
        return True
    else:
        return False


def test_db_exists():
    assert check_db_exists() == True


def check_columns_exists():
    if Clients.select(
        Clients.name, Clients.city, Clients.address
    ) and Orders.select(
        Orders.client_id, Orders.date, Orders.amount, Orders.description
    ):
        return True
    else:
        return False


def test_columns_exists():
    assert check_columns_exists() == True


def check_records_count():
    if Clients.select().count() >= 10 and Orders.select().count() >= 10:
        return True
    else:
        return False


def test_record_count():
    assert check_records_count() == True
