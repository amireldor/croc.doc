from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text


Base = declarative_base()


class Docs(Base):
    """
    A piece of user submitted data that was given a shortened URL.
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    created = Column(DateTime(timezone=True))
    updated = Column(DateTime(timezone=True))
    expires = Column(DateTime(timezone=True))
    type = Column(String(30))  # "text" or other that will be used in the future (code/link/file/...)
    body = Column(Text)
