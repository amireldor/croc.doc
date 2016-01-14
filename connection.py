"""
Connection to the database. MongoDB?
"""

from pymongo import MongoClient

client = MongoClient()
database = client.docs
docs = database.docs
