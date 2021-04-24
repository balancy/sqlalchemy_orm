from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(bind=engine, autoflush=False)
Session = scoped_session(session_factory)

Base = declarative_base()
Base.query = Session.query_property()
