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

class TestAdminUsersFunctional(unittest.TestCase):

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
        super(TestAdminUsersFunctional, self).setUp()

    def test_users_list(self):
        result = self.app.get('/admin/users', status=200)
        content = """<td>MF Jones</td>"""
        asserting = content in str(result.body)
        self.assertEqual(asserting, True, asserting)


class TestAdminTeamsFunctional(unittest.TestCase):

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
        super(TestAdminTeamsFunctional, self).setUp()

    def test_teams_list(self):
        result = self.app.get('/admin/teams', status=200)
        content = """<td>Linux</td>"""
        asserting = content in str(result.body)
        self.assertEqual(asserting, True, asserting)