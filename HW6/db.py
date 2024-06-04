from datetime import datetime

import sqlalchemy
from sqlalchemy import (
    DECIMAL,
    Date,
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
    MetaData,
    create_engine,
)
import databases as databases
from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = MetaData()

users = sqlalchemy.Table(
    'users',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('first_name', sqlalchemy.String(32)),
    sqlalchemy.Column('last_name', sqlalchemy.String(32)),
    sqlalchemy.Column('birth_date', sqlalchemy.Date()),
    sqlalchemy.Column('address', sqlalchemy.String(255)),
    sqlalchemy.Column('email', sqlalchemy.String(128)),
    sqlalchemy.Column('password', sqlalchemy.String(255))
)

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("price", DECIMAL),
)

orders = Table(
    'orders',
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("item_id", Integer, ForeignKey("items.id")),
    Column("order_date", String(64), nullable=False, default=datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
           onupdate=datetime.now().strftime("%d/%m/%y, %H:%M:%S")),
    Column("status", String(24), server_default='created'),
)

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})

metadata.create_all(engine)
