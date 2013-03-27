import unittest
import transaction

from pyramid import testing

from ..models import DBSession
from ..models import Base
from ..models import User

class TestHome(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from ..models import (
            DBSession,
            User,
            Membership,
        )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            user = [
                User(username='djohansen', name='djohansen', email="djohansen@admin.com"),
                User(username='tgraham', name='tgraham', email="tgraham@admin.com")
            ]
            DBSession.add_all(user)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_it(self):
        from ..views.home import home_page
        request = testing.DummyRequest()
        info = home_page(request)
        self.assertEqual(info['project'], 'creme fraiche')