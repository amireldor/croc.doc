"""
This module is responsible for:
    - Generating new unique doc names
    - rabbits
"""

from random import randint, choice
import datetime
from connection import docs as docs_collection
import pymongo

adjectives = list(map(lambda w: w.strip().lower(), open('Adjectives.txt').readlines()))
animals = list(map(lambda w: w.strip().lower(), open('Animals.txt').readlines()))

def randomDocName():
    """Returns a random doc name.  You should actually call `uniqueDocName`.
    """
    final = "{}-{}-{}".format( choice(adjectives), choice(animals), str(randint(0, 1000)).zfill(3) )
    return final


class NoDocFound(Exception):
    pass

class DatabaseError(Exception):
    pass

def getDoc(name):
    try:
        doc = docs_collection.find_one({ "name": name });
        if doc is None:
            raise NoDocFound("Can't find a doc named %s" % name)

    except pymongo.errors.ConnectionFailure:
        raise DatabaseError("Couldn't connect to database")


    return doc


def saveDoc(doc):
    """Attemps to save the doc.  If duplicate key, try again with differnet
    key, or in other words, fuck the duck until exploded.  Will bail after
    several tries Will bail after several tries.

    Return the newly created doc name, or None for failure
    """
    data = {
        "name": None,
        "doc": doc,
        "inserted": datetime.datetime.utcnow()
    }

    for _ in range(10):
        try:
            name = randomDocName()
            data['name'] = name
            docs_collection.insert_one(data)
            return name

        except pymongo.errors.DuplicateKeyError:
            pass

    return None
