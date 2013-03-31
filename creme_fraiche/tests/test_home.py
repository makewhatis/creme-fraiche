import os
import unittest
import transaction

from pyramid import testing
from webtest import TestApp

from paste.deploy.loadwsgi import appconfig

from creme_fraiche.models import DBSession
from creme_fraiche.models import Base
from creme_fraiche.models import Users
from creme_fraiche.models import Teams


class TestHome(unittest.TestCase):

    def test_it(self):
        from ..views.home import home_page
        request = testing.DummyRequest()
        info = home_page(request)
        self.assertEqual(info['project'], 'creme fraiche')


class TestHomeFunctional(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        here = os.path.dirname(__file__)
        settings = appconfig(
            'config:' + os.path.join(here, './', 'test.ini')
        )
        from creme_fraiche import main        
        cls.app = main({}, **settings)

    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(TestHomeFunctional, self).setUp()

    def test_home(self):
        result = self.app.get('/', status=200)
        content = """<li>MF Jones</li>"""
        asserting = content in str(result.body)
        self.assertEqual(asserting, True, asserting)