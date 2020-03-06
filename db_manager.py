from constants import *
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import sqlite3
from models import *


class DBManager:
    engine = None
    Session = None
    ScopedSession = None

    @staticmethod
    def init():
        # TODO: Turn off echo
        DBManager.engine = create_engine('sqlite:///{}'.format(DB_FILE), echo=True)

        @event.listens_for(DBManager.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if type(dbapi_connection) is sqlite3.Connection:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        DBManager.Session = sessionmaker(bind=DBManager.engine, autoflush=True)
        DBManager.ScopedSession = scoped_session(sessionmaker(bind=DBManager.engine))

    @staticmethod
    def create_session(**options):
        if DBManager.engine is None:
            DBManager.init()
        return DBManager.Session(**options)

    @staticmethod
    @contextmanager
    def create_session_scope(**options):
        session = DBManager.create_session(**options)
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def initialize():
        """ Creates all tables """
        Base.metadata.create_all(DBManager.engine)

    @staticmethod
    def reinitialize():
        """ Drops all tables and creates them again """
        Base.metadata.drop_all(DBManager.engine, checkfirst=True)
        DBManager.initialize()


if __name__ == '__main__':
    DBManager.init()
    DBManager.reinitialize()
    with DBManager.create_session_scope() as session:
        print(session.query(Contact).all())
