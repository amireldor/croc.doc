import unittest
import docs
import connection
from db.models import Base
import datetime


class DocsTestCase(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(bind=connection.engine)

    def tearDown(self):
        pass

    def test_save_doc(self):
        test_doc_name = 'bunnies'

        with self.assertRaises(docs.NoDocFound):
            docs.get_doc(test_doc_name)

        docs.save_doc('I like bunnies', name=test_doc_name)
        self.assertIsNotNone(docs.get_doc(test_doc_name))

        docs.delete_doc(test_doc_name)

    def test_delete_doc(self):
        test_doc_name = 'homies'

        with self.assertRaises(docs.NoDocFound):
            docs.get_doc(test_doc_name)

        docs.save_doc("poc", name=test_doc_name)
        self.assertIsNotNone(docs.get_doc(test_doc_name))
        docs.delete_doc(test_doc_name)

        with self.assertRaises(docs.NoDocFound):
            docs.get_doc(test_doc_name)

    def test_dont_save_on_not_expired_doc(self):
        test_doc_name = 'testing123'

        now = datetime.datetime.utcnow()
        expires = now + datetime.timedelta(days=10)
        docs.save_doc('Testing', name=test_doc_name, expires=expires)

        with self.assertRaises(docs.DocNotExpired):
            docs.save_doc("Shouldn't save", name=test_doc_name)

        docs.delete_doc(test_doc_name)

    def test_save_on_expired_doc(self):
        test_doc_name = 'testing catman3'

        now = datetime.datetime.utcnow()
        expires = now - datetime.timedelta(days=10)
        docs.save_doc('Can I play with Catman?', name=test_doc_name, expires=expires)

        new_body = "The wind and the sea and the sand"
        docs.save_doc(new_body, name=test_doc_name)
        new_doc = docs.get_doc(test_doc_name)
        self.assertEqual(new_body, new_doc['body'])

        docs.delete_doc(test_doc_name)

    def test_random_doc_name_existed(self):
        self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()