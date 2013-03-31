import unittest
import mock
from pyramid import testing


class TestSecurity(unittest.TestCase):

    def test_groupfinder_user(self):
        from creme_fraiche.security import groupfinder

        user = groupfinder('admin', None)
        self.assertEqual(
            user,
            ['admin', 'user'],
            "Did not return correct id: %s" % user
        )

    def test_groupfinder_not_user(self):
        from creme_fraiche.security import groupfinder

        user = groupfinder('tim', None)
        self.assertEqual(
            user,
            ['user'],
            "Shuld return user."
        )

    def test_groupfinder_fail_add(self):
        from creme_fraiche.security import groupfinder
        from creme_fraiche.security import add_entry
        from creme_fraiche.models import DBSession
        from sqlalchemy.exc import DBAPIError

        obj = mock.Mock()
        with mock.patch.object(DBSession, 'add') as sess:
                sess.side_effect = DBAPIError(None, None, 'ERROR')
                results = add_entry(obj)
        self.assertEqual(results, False, "This should return False")
