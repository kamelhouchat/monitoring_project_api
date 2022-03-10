""""
SQLAlchemy ORM
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

# DB Session
SESSION_FACTORY = sessionmaker(autocommit=False, autoflush=False)
DB_SESSION = scoped_session(SESSION_FACTORY)
Base = declarative_base()


class DBConnection:
    """
    Databases accessories
    """

    def __init__(self):
        self.sqla_engine = None

    def set_sqla_db_url(self, db_url):
        """Set DB URL"""
        self.sqla_engine = create_engine(
            db_url, future=True, connect_args={'check_same_thread': False})
        SESSION_FACTORY.configure(bind=self.sqla_engine)

    @property
    def session(self):
        return DB_SESSION

    @property
    def url(self):
        return self.sqla_engine.url if self.sqla_engine else None

    def sqla_create_all(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.sqla_engine)

    def sqla_drop_all(self):
        """Drop all tables"""
        Base.metadata.drop_all(bind=self.sqla_engine)

    def sqla_setup_tables(self):
        """Recreate database tables"""
        self.sqla_drop_all()
        self.sqla_create_all()

    def dispose(self):
        self.sqla_engine.dispose()
        self.sqla_engine = None

    def close(self):
        self.session.close()


db = DBConnection()


def init_app(app):
    """Init DB accessories with app

    Sets DB engine using app config.
    Adds app contextTeardown method to close DB session.
    """

    db.set_sqla_db_url(app.config["SQLALCHEMY_DATABASE_URI"])

    @app.teardown_appcontext
    def cleanup(_):
        db.session.remove()
