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

from creme_fraiche.views.admin.users import admin_create_user
from creme_fraiche.views.admin.users import admin_create_user_post


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

    def _callFUT(self, func, request):
        return func(request)

    def test_users_list(self):
        result = self.app.get('/admin/users', status=200)
        content = """Login"""
        asserting = content in str(result.body)
        self.assertEqual(asserting, True, asserting)

    def test_admin_create_user(self):
        admin = testing.DummyResource()
        admin['admin_user_create'] = testing.DummyResource()

        request = testing.DummyRequest()
        request.matched_route = testing.DummyRequest()
        request.matched_route.name = 'admin_user_create'

        request.session = testing.DummyRequest()
        request.session['username'] = 'admin'
        request.logged_in = True
        info = self._callFUT(admin_create_user, request)
        self.assertEqual(
            info['users'][0].username,
            'admin',
            info
        )

    def test_admin_create_user_post(self):
        admin = testing.DummyResource()
        admin['admin_create_user'] = testing.DummyResource()

        self.config = testing.setUp()
        self.config.add_route('admin_create_user', '/admin/user/create')
        self.config.add_route('admin_list_users', '/admin/users')

        request = testing.DummyRequest(post={
            'submit': True,
        })
        #request.matched_route = testing.DummyRequest()
        #request.matched_route.name = 'admin_create_user_post'

        request.session = testing.DummySession()

        request.session['username'] = 'admin'
        info = self._callFUT(admin_create_user_post, request)


def _registerRoutes(config):
    config.add_route('admin_create_user', '/admin/users/create')
    config.add_route('admin_list_users', '/admin/users')


def _registerCommonTemplates(config):
    config.testing_add_renderer('templates/includes/header.html')
    config.testing_add_renderer('templates/includes/footer.html')


class TestAdminTeamsFunctional(unittest.TestCase):

    admin_login = '/login?username=admin&password=admin' \
        '&came_from=home_page&form.submitted=login'
    viewer_wrong_login = '/login?username=viewer&password=incorrect' \
        '&came_from=home_page&form.submitted=login'

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

    def _login(self):
        res = self.app.get(self.admin_login)
        self.assertTrue(res.status_code is 200)
        form = res.form
        form['username'] = 'admin'
        form['password'] = 'letmein'
        res = form.submit('submit')
        return res

    def test_teams_list(self):
        result = self.app.get('/admin/teams', status=200)
        content = """Login"""
        asserting = content in str(result.body)
        self.assertEqual(asserting, True, asserting)

    def test_admin_list_users(self):
        _registerRoutes(self.config)
        _registerCommonTemplates(self.config)
        #login
        res = self._login()
        res = self.app.get('/admin/users', status=200)

        self.assertTrue('<h2>List Users</h2>' in res)
        self.assertTrue(res.status_code is 200)

    def test_admin_create_user_post_fail(self):
        _registerRoutes(self.config)
        _registerCommonTemplates(self.config)
        #login
        res = self._login()

        res = self.app.get('/admin/users/create')
        self.assertTrue(res.status_code is 200)
        form = res.form
        form['username'] = 'admin'
        form['fullname'] = 'Mr Admin'
        form['email'] = 'admin@email'
        res = form.submit('submit')

        self.assertTrue('302 Found' in res)
        self.assertEqual(res.status_int, 302, res)

        res = self.app.get('/admin/users/create')
        self.assertTrue(res.status_code is 200)
        form = res.form
        form['username'] = 'admin'
        form['email'] = 'admin@email'

        res = form.submit('submit')
        self.assertTrue('302 Found' in res)

    def test_admin_create_user_create_delete(self):
        _registerRoutes(self.config)
        _registerCommonTemplates(self.config)
        #login
        res = self._login()

        res = self.app.get('/admin/users/create')
        self.assertTrue(res.status_code is 200)
        form = res.form
        form['username'] = 'user1'
        form['fullname'] = 'Mr User1'
        form['email'] = 'user1@email'
        res = form.submit('submit')
        print res
        self.assertTrue('302 Found' in res)

        res = self.app.get('/admin/users')
        self.assertTrue('user1' in res)

        res = self.app.get('/admin/user/delete/2')
        self.assertEqual(res.status_int, 302, res)
        self.assertTrue('user1' not in res)

        res = self.app.get('/admin/user/delete/21')
        self.assertEqual(res.status_int, 302, res)

