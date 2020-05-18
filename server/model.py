import os

from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import ForeignKey
from sqlalchemy.types import Integer, String, Boolean, Text, DateTime
from sqlalchemy.pool import StaticPool

from datetime import datetime


__all__ = [
    "Model",
    "Account",
    "Question",
    ]


class Model:
    _models = [
        "Account",
        "Question",
    ]
    meta = None
    engine = None
    conn = None

    @classmethod
    def start_engine(cls, db_uri=None):
        if db_uri is None:
            cls.engine = create_engine(
                "sqlite:///:memory:",
                connect_args={'check_same_thread': False},
                poolclass=StaticPool
                )
        else:
            cls.engine = create_engine(db_uri)

    @classmethod
    def initial_meta(cls):
        cls.meta = MetaData()

        for name in cls._models:
            model = eval(name)
            model.register(cls.meta)

        cls.meta.create_all(cls.engine)
    
    @classmethod
    def connect(cls):
        cls.conn = cls.engine.connect()
        return cls.conn
    
    @classmethod
    def disconnect(cls):
        if cls.conn is not None:
            cls.conn.close()
            cls.conn = None


class Account:
    NAME = "tb-account"
    T = None

    @classmethod
    def register(cls, meta):
        cls.T = Table(
            cls.NAME,
            meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("login_id", String, nullable=False, autoincrement=False,
                   unique=True),
            Column("password", String, nullable=False, autoincrement=False),
            Column("create_at", DateTime, default=datetime.utcnow,
                   autoincrement=True),
            )


class Question:
    NAME = "tb-question"
    T = None

    @classmethod
    def register(cls, meta):
        cls.T = Table(
            cls.NAME,
            meta,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("title", String, nullable=False, autoincrement=False),
            Column("content", Text, nullable=False, autoincrement=False),
            Column("writer", String, nullable=False, autoincrement=False),
            Column("create_at", DateTime, default=datetime.now,
                   autoincrement=True),
            )


if __name__ == "__main__":
    Model.start_engine("sqlite:///test.db")
    Model.initial_meta()

    if os.path.isfile("test.db"):
        os.remove("test.db")
