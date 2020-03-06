from constants import DB_FILE
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import sqlite3
from models import *


class DBManager:
    """
        Singleton class for managing database connections using SQLAlchemy session
        :attr engine: Database Engine for SQLAlchemy
        :attr Session: Manages persistence operations for ORM-mapped objects
    """
    engine = None
    Session = None

    @staticmethod
    def init():
        # Initialize engine with SQLite
        DBManager.engine = create_engine('sqlite:///{}'.format(DB_FILE), echo=False)

        @event.listens_for(DBManager.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """
                Sets foreign_keys to ON in SQLite
                By default it is OFF
            """
            if type(dbapi_connection) is sqlite3.Connection:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        DBManager.Session = sessionmaker(bind=DBManager.engine, autoflush=True)

    @staticmethod
    def create_session(**options):
        """
            Returns a Session object with optional options
            :param options: Configurable options like autoflush, autocommit
        """
        if DBManager.engine is None:
            DBManager.init()
        return DBManager.Session(**options)

    @staticmethod
    @contextmanager
    def create_session_scope(**options):
        """
            Returns a Session for context manager
            Commits and closes the session when exiting the context manager
            Rollback when exception occurs
        """
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
        """
            Creates all tables defined in Models
        """
        Base.metadata.create_all(DBManager.engine)

    @staticmethod
    def reinitialize():
        """
            Drops all tables and creates them again
            Method can be used to purge all data
        """
        Base.metadata.drop_all(DBManager.engine, checkfirst=True)
        DBManager.initialize()


if __name__ == '__main__':
    DBManager.init()
    DBManager.reinitialize()
    with DBManager.create_session_scope() as session:
        print("Database Reinitialized", session.query(Contact).all())
