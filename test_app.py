import os
import pytest
from peewee import *
from app import init, fill, Clients, Orders


DB_NAME = "Database.db"


def test_db_exists():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    init()
    assert os.path.exists(DB_NAME) == True


def test_columns_exists():
    fill()
    assert (
        Clients.select(Clients.name, Clients.city, Clients.address) == True
        and Orders.select(
            Orders.client_id, Orders.date, Orders.amount, Orders.description
        )
        == True
    )


def test_records_count():
    assert len(Clients.select()) >= 10 and len(Orders.select()) >= 10
