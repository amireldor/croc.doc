"""
Connection to the database.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:@localhost:5432/crocfarm')

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

session = Session()
