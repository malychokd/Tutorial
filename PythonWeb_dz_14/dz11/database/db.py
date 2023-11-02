from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker

from dz11.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    """
    The get_db function opens a new database connection if there is none yet for the current application context.
    It will also create the database tables if they don’t exist yet.
    
    :return: A database sessionlocal object
    :doc-author: Trelent
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()