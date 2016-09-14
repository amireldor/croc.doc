from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text, Enum

Base = declarative_base()


class Animal(Base):
    """
    Croc feeds upon animals.  This is the actual data of the objects submitted by users.
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    created = Column(DateTime, timezone=True)
    updated = Column(DateTime, timezone=True)
    expires = Column(DateTime, timezone=True)
    type = Column(Enum(enums=['text', 'link', 'code', 'file']))  # We start with text only
    body = Column(Text)
