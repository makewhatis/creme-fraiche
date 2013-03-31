from creme_fraiche.models import get_role
from creme_fraiche.models import get_user_by_username
from creme_fraiche.models import get_users_roles
from creme_fraiche.models import DBSession
from creme_fraiche.models import Users
from creme_fraiche.models import Role_Membership
from sqlalchemy.exc import DBAPIError

import logging
log = logging.getLogger(__name__)


def add_entry(obj):
    try:
        DBSession.add(obj)
    except DBAPIError as e:
        log.error("Error adding user: %s" % e)
        return False


def groupfinder(username, request):
    user = get_user_by_username(username)
    if not user:
        user_role = get_role('user')
        new_user_ojb = Users(
            username=username,
            fullname=username,
            email="%s@example.com" % username
        )
        add_entry(new_user_ojb)

        new_user = get_user_by_username(username)

        new_member_obj = Role_Membership(
            role_id=user_role.id,
            user_id=new_user.id
        )

        add_entry(new_member_obj)

        return get_users_roles(new_user.id)
    else:
        existing_user = get_user_by_username(username)
        return get_users_roles(existing_user.id)
