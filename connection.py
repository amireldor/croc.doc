"""
Connection to the database. MongoDB?
"""
import os
from pymongo import MongoClient

# 'mongo' host should be docker stuff from docker-compose
connection_url = os.environ.get('CONNECTION_URL', 'mongodb://mongo')

client = MongoClient(connection_url)
database = client.docs
docs = database.docs
