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
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
adjectives = [w.strip().lower() for w in open(os.path.join(SCRIPT_DIR, 'Adjectives.txt')).readlines()]
animals = [w.strip().lower() for w in open(os.path.join(SCRIPT_DIR, 'Animals.txt')).readlines()]

tz_utc = pytz.timezone('UTC')


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


class DocSaver:

    AUTO_CALCULATE_EXPIRY = 'auto_calculate_expirt'

    def __init__(self):
        self.doc = None
        self.name = ''
        self.expires = DocSaver.AUTO_CALCULATE_EXPIRY

    def save_doc(self, body, name, try_other_names=True, expires=AUTO_CALCULATE_EXPIRY):
        self.expires = expires
        for _ in range(settings.SAVE_RETRIES):
            self.name = name
            self.doc = session.query(Doc).filter(Doc.name == self.name).one_or_none()
            try:
                self.save_or_update_doc(body)

            except DocNotExpired as exception:
                if try_other_names:
                    continue
                else:
                    raise exception

            session.add(self.doc)
            session.commit()
            return self.name

        # If we reach here, the SAVE_RETRIES loop finished and something is bad
        raise FailedToSave('Reached maximum save retry count, seems like many docs exist today!')

    def save_or_update_doc(self, body):
        now = tz_utc.localize(datetime.datetime.utcnow())
        if self.doc is not None:
            expired = now > tz_utc.localize(self.doc.expires)
            if not expired:
                raise DocNotExpired
            self.doc.updated = now
            self.doc.body = body
        else:
            self.doc = Doc(name=self.name,
                           created=now,
                           updated=now,
                           type="text",  # only "text" supported for now
                           body=body,
                           )
        if self.expires == DocSaver.AUTO_CALCULATE_EXPIRY:
            self.doc.calculate_expiry_time()
        else:
            self.doc.expires = self.expires


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


def save_doc(body, name=None, expires=DocSaver.AUTO_CALCULATE_EXPIRY):
    """
    If no name is provided, randomize a name until an available name is found.
    If name is provided, then try to save only that name and don't randomize any further. This is `try_once`!
    """
    if name is None:
        name = random_doc_name()
        try_other_names = True
    else:
        try_other_names = False

    saver = DocSaver()
    saver.save_doc(body, name=name, try_other_names=try_other_names, expires=expires)


def delete_doc(name):
    doc = session.query(Doc).filter(Doc.name == name).one_or_none()
    if doc is not None:
        session.delete(doc)
        session.commit()


