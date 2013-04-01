import unittest
import mock
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


class TestModelReportFormats(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import ReportFormats
        return ReportFormats

    def _makeOne(self):
        return self._getTargetClass()(
            name='html'
        )

    def test_formats(self):
        formats = self._makeOne()
        self.assertEqual(formats.name, 'html')
        self.assertEqual(formats.__repr__(), "ReportFormats('html')")


class TestModelReportTemplates(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import ReportTemplates
        return ReportTemplates

    def _makeOne(self):
        return self._getTargetClass()(
            name='ops',
            style=".clearfix {*zoom: 1;]"
        )

    def test_templates(self):
        templates = self._makeOne()
        self.assertEqual(templates.name, 'ops')
        self.assertEqual(templates.style, ".clearfix {*zoom: 1;]")
        self.assertEqual(templates.__repr__(), "ReportTemplates('ops')")


class TestModelReports(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import Reports
        return Reports

    def _makeOne(self):
        from datetime import datetime
        self.time = datetime.now()
        return self._getTargetClass()(
            team_id=1,
            template_id=1,
            format_id=1,
            report_time=self.time
        )

    def test_templates(self):
        reports = self._makeOne()
        self.assertEqual(reports.team_id, 1)
        self.assertEqual(reports.report_time, self.time)
        self.assertEqual(reports.template_id, 1)
        self.assertEqual(reports.format_id, 1)


class TestModelPermissionTypes(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import PermissionTypes
        return PermissionTypes

    def _makeOne(self):
        return self._getTargetClass()(
            name='read'
        )

    def test_formats(self):
        permission_types = self._makeOne()
        self.assertEqual(permission_types.name, 'read')
        self.assertEqual(
            permission_types.__repr__(),
            "PermissionTypes('read')"
        )


class TestModelCategory(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import Category
        return Category

    def _makeOne(self):
        return self._getTargetClass()(
            name='projects',
            parent_id=1,
            team_id=1
        )

    def test_templates(self):
        category = self._makeOne()
        self.assertEqual(category.name, 'projects')
        self.assertEqual(category.parent_id, 1)
        self.assertEqual(category.team_id, 1)
        self.assertEqual(
            category.__repr__(),
            "Category(projects)"
        )


class TestModelEntry(unittest.TestCase):

    def _getTargetClass(self):
        from creme_fraiche.models import Entry
        return Entry

    def _makeOne(self):
        from datetime import datetime
        self.time = datetime.now()
        return self._getTargetClass()(
            data='what is a data',
            user_id=1,
            cat_id=1,
            team_id=1,
            entry_time=self.time
        )

    def test_templates(self):
        entry = self._makeOne()
        self.assertEqual(entry.data, 'what is a data')
        self.assertEqual(entry.user_id, 1)
        self.assertEqual(entry.cat_id, 1)
        self.assertEqual(entry.team_id, 1)
        self.assertEqual(entry.entry_time, self.time)
        self.assertEqual(
            entry.__repr__(),
            "Entry(what is a data)"
        )


class TestModel(unittest.TestCase):

    def test_get_team(self):
        from creme_fraiche.models import get_team

        team = get_team('Linux')
        self.assertEqual(team.id, 1, "Team not 1")
        self.assertEqual(team.name, 'Linux', "Name not Linux")

    def test_get_role(self):
        from creme_fraiche.models import get_role
        from creme_fraiche.models import DBSession
        from sqlalchemy.exc import DBAPIError

        role = get_role('user')
        self.assertEqual(role.id, 2, "Role id not 2: %s" % role.id)
        self.assertEqual(role.name, 'user', "Name not user")

        with mock.patch.object(DBSession, 'query') as sess:
                sess.side_effect = DBAPIError(None, None, 'ERROR')
                results = get_role('user')

    def test_get_team(self):
        from creme_fraiche.models import get_team
        from creme_fraiche.models import DBSession
        from sqlalchemy.exc import DBAPIError

        team = get_team('Linux')
        self.assertEqual(team.id, 1, "Team id not 1: %s" % team.id)
        self.assertEqual(team.name, 'Linux', "Name not Linux")

        with mock.patch.object(DBSession, 'query') as sess:
                sess.side_effect = DBAPIError(None, None, 'ERROR')
                results = get_team('Linux')

    def test_get_user_by_name(self):
        from creme_fraiche.models import get_user_by_username
        from creme_fraiche.models import DBSession
        from sqlalchemy.exc import DBAPIError

        user = get_user_by_username('admin')
        self.assertEqual(user.id, 1, "User id not 1: %s" % user.id)
        self.assertEqual(user.fullname, 'MF Jones', "Name not MF Jones")

        with mock.patch.object(DBSession, 'query') as sess:
                sess.side_effect = DBAPIError(None, None, 'ERROR')
                results = get_user_by_username('admin')

    def test_get_user_by_id(self):
        from creme_fraiche.models import get_user_by_id
        from creme_fraiche.models import DBSession
        from sqlalchemy.exc import DBAPIError

        user = get_user_by_id(1)
        self.assertEqual(user.id, 1, "User not 1: %s" % user.id)
        self.assertEqual(user.fullname, 'MF Jones', "Name not MF Jones")
        self.assertEqual(user.username, 'admin', "username not admin")

        with mock.patch.object(DBSession, 'query') as sess:
                sess.side_effect = DBAPIError(None, None, 'ERROR')
                results = get_user_by_id(1)

    def test_fail_get_users_roles(self):
        from creme_fraiche.models import get_users_roles
        from creme_fraiche.models import DBSession
        from sqlalchemy.exc import DBAPIError

        with mock.patch.object(DBSession, 'query') as sess:
                sess.side_effect = DBAPIError(None, None, 'ERROR')
                roles = get_users_roles(1)
        self.assertEqual(roles, False, "Did not fail and return False")
