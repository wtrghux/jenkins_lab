import time
import random
import argparse
from sys import exit
from datetime import date
from inflect import engine
from prettytable import PrettyTable
from peewee import *

pt = PrettyTable()
p = engine()


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("arg_1", nargs="?")
    parser.add_argument("arg_2", nargs="?")
    return parser


db = SqliteDatabase("Database.db")


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


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d", prop)


def init():
    if Clients.table_exists() == False and Orders.table_exists() == False:
        db.create_tables([Clients, Orders])
    else:
        db.drop_tables([Clients, Orders])
        db.create_tables([Clients, Orders])
    db.close()


def fill():
    for _ in range(10):
        client = Clients(
            name=p.number_to_words(random.randint(1, 100)),
            city=p.number_to_words(random.randint(1, 100)),
            address=p.number_to_words(random.randint(1, 100)),
        )
        client.save()
        order = Orders(
            client=p.number_to_words(random.randint(1, 100)),
            date=random_date("2020-01-01", "2021-02-25", random.random()),
            amount=random.randint(1, 100),
            description=p.number_to_words(random.randint(1, 100)),
        )
        order.save()
        db.commit()
    db.close()


def help_():
    print(
        """
Справка:
– запуск с параметром `init` инициализирует базу данных
– запуск с параметром `fill` заполнит базу данных тестовыми значениями
– запуск с параметром `show [tablename]` выведет указанную таблицу"""
    )
    exit()


def show_clients(Clients):
    query = Clients.select(
        Clients.id, Clients.name, Clients.city, Clients.address
    )
    pt.field_names = ["id", "name", "city", "address"]
    for Clients in query:
        pt.add_row([Clients.id, Clients.name, Clients.city, Clients.address])
    print(pt)


def show_orders(Orders):
    query = Orders.select(
        Orders.id,
        Orders.client_id,
        Orders.date,
        Orders.amount,
        Orders.description,
    )
    pt.field_names = ["id", "client_id", "date", "amount", "description"]
    for Orders in query:
        pt.add_row(
            [
                Orders.id,
                Orders.client_id,
                Orders.date,
                Orders.amount,
                Orders.description,
            ]
        )
    print(pt)


if __name__ == "__main__":

    args = createParser().parse_args()
    cursor = db.cursor()

    if args.arg_1 == "init":
        init()
    elif args.arg_1 == "fill":
        fill()
    elif args.arg_1 == "show":
        if (args.arg_2).lower() == "clients":
            show_clients(Clients)
        elif (args.arg_2).lower() == "orders":
            show_orders(Orders)
        else:
            print("This table does not exist")
    else:
        help_()

    db.close()
