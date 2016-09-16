"""
This module is responsible for:
    - Generating new unique doc names
    - rabbits
"""

from random import choice
import datetime
from connection import session
from db.models import Doc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import settings

adjectives = [w.strip().lower() for w in open('Adjectives.txt').readlines()]
animals = [w.strip().lower() for w in open('Animals.txt').readlines()]


def random_doc_name():
    final = "{}-{}".format( choice(adjectives), choice(animals) )
    return final


class NoDocFound(Exception):
    pass


class DatabaseError(Exception):
    pass


class FailedToSave(Exception):
    pass


def get_doc(name):
    try:
        # doc = docs_collection.find_one({ "name": name });
        doc = session.query(Doc).filter(Doc.name == name).one()
        json_doc = {
            'name': doc.name,
            'doc': doc.body,
            'type': doc.type,
        }
        return json_doc

    except NoResultFound:
        raise NoDocFound("Can't find a doc named {}".format(name))

    except MultipleResultsFound:
        raise DatabaseError("Multiple entries to doc {}, something is terribly wrong".format(name))

    return None


def save_doc(doc):
    """Saves the doc.  If name exists in database and is not protected,
    overwrite the existing doc.  If the name exists and is protected (was used
    recently), then try a differnet name.

    Return the newly created doc name, or None on failure.
    """
    for _ in range(settings.SAVE_RETRIES):
        try:
            name = random_doc_name()
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
