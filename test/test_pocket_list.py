import logging
import unittest
from readpick.readlists.pocket import Pocket
import readpick.ebook.model as model


class PocketAccessTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(format="[%(name)s] %(levelname)s: %(message)s",
                            level=logging.DEBUG)

    def test_authorize_session(self):
        pocket = Pocket()
        self.assertIsNone(pocket.access_token)
        pocket.authorize_session()
        self.assertIsNotNone(pocket.access_token)


if __name__ == '__main__':
    unittest.main()