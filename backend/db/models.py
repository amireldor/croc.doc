from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, Integer, String, Text
import settings
import datetime


Base = declarative_base()


class Doc(Base):
    """
    A piece of user submitted data that was given a shortened URL.
    """
    __tablename__ = "docs"
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    created = Column(DateTime(timezone=True))
    updated = Column(DateTime(timezone=True))
    expires = Column(DateTime(timezone=True))
    type = Column(String(30))  # "text" or other that will be used in the future (code/link/file/...)
    body = Column(Text)

    def calculate_expiry_time(self):
        self.expires = self.updated + datetime.timedelta(seconds=settings.SECONDS_TO_EXPIRE)
