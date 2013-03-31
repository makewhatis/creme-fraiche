import unittest

from pyramid import testing


class TestModelUsers(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import Users
        return Users

    def _makeOne(self):
        return self._getTargetClass()(
            username='bob',
            fullname='bob jones',
            email='bob@email.com'
        )

    def test_users(self):
        user = self._makeOne()
        self.assertEqual(user.username, 'bob')
        self.assertEqual(user.fullname, 'bob jones')
        self.assertEqual(user.email, 'bob@email.com')
        self.assertEqual(user.__repr__(), "Users('bob')")


class TestModelRoles(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import Roles
        return Roles

    def _makeOne(self):
        return self._getTargetClass()(
            name='admin'
        )

    def test_roles(self):
        roles = self._makeOne()
        self.assertEqual(roles.name, 'admin')
        self.assertEqual(roles.__repr__(), "Roles('admin')")


class TestModelTeams(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import Teams
        return Teams

    def _makeOne(self):
        return self._getTargetClass()(
            name='Linux'
        )

    def test_teams(self):
        teams = self._makeOne()
        self.assertEqual(teams.name, 'Linux')
        self.assertEqual(teams.__repr__(), "Teams('Linux')")


