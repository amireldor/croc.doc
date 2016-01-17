"""
This module is responsible for:
    - Generating new unique doc names
    - rabbits
"""

from random import randint, choice
import datetime
from connection import docs as docs_collection
import pymongo
import settings

adjectives = list(map(lambda w: w.strip().lower(), open('Adjectives.txt').readlines()))
animals = list(map(lambda w: w.strip().lower(), open('Animals.txt').readlines()))

def randomDocName():
    final = "{}-{}".format( choice(adjectives), choice(animals) )
    return final


class NoDocFound(Exception):
    pass

class DatabaseError(Exception):
    pass

class FailedToSave(Exception):
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
    """Saves the doc.  If name exists in database and is not protected,
    overwrite the existing doc.  If the name exists and is protected (was used
    recently), then try a differnet name.

    Return the newly created doc name, or None on failure.
    """
    for _ in range(settings.SAVE_RETRIES):
        try:
            name = randomDocName()
            doc_in_db = docs_collection.find_one({ "name": name }, { "protected_until": 1 });

            if doc_in_db is None:
                exists = False
            else:
                exists = True

            try:
                if exists and doc_in_db["protected_until"] >= datetime.datetime.utcnow():
                    # Still under protection
                    continue # Search another name

            except KeyError:
                # No protected_until key
                pass

            # OK, save or update it
            data = {
                "name": name,
                "doc": doc,
                "inserted": datetime.datetime.utcnow(),
                "protected_until": datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.PROTECTION_TIME),
            }

            docs_collection.update_one({"name": name}, {"$set": data}, upsert=True)

            # Save successful!
            return name

        except pymongo.errors.DuplicateKeyError:
            pass

    # Failed to save
    raise FailedToSave('Reached maximum save retry count, seems like many docs are protected today!')
