"""
This module is responsible for:
    - Generating new unique doc names
    - rabbits
"""

from random import choice
from connection import session
from db.models import Doc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import settings
import datetime
import pytz

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


class DocNotExpired(Exception):
    pass


def get_doc(name):
    try:
        # doc = docs_collection.find_one({ "name": name });
        doc = session.query(Doc).filter(Doc.name == name).one()
        json_doc = {
            'name': doc.name,
            'body': doc.body,
            'type': doc.type,
        }
        return json_doc

    except NoResultFound:
        raise NoDocFound("Can't find a doc named {}".format(name))

    except MultipleResultsFound:
        raise DatabaseError("Multiple entries to doc {}, something is terribly wrong".format(name))

    return None


class DocSaver:
    def __init__(self):
        self.doc = None
        self.name = ''

    def save_doc(self, body):
        for _ in range(settings.SAVE_RETRIES):
            self.name = random_doc_name()
            self.doc = session.query(Doc).filter(Doc.name == self.name).one_or_none()
            try:
                self.save_or_update_doc(body)
            except DocNotExpired:
                continue
            session.add(self.doc)
            session.commit()
            return self.name

        # If we reach here, the SAVE_RETRIES loop finished and something is bad
        raise FailedToSave('Reached maximum save retry count, seems like many docs exist today!')

    def save_or_update_doc(self, body):
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)
        if self.doc is not None:
            expired = now > self.doc.expires
            if not expired:
                raise DocNotExpired
            self.doc.updated = now
        else:
            self.doc = Doc(name=self.name,
                           created=now,
                           updated=now,
                           type="text",  # only "text" supported for now
                           body=body,
                           )
        self.doc.calculate_expiry_time()
