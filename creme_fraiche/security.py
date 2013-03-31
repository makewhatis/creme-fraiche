from .models import get_group
from .models import get_user
from .models import get_users_groups
from .models import DBSession
from .models import Users
from .models import Role_Membership
from sqlalchemy.exc import DBAPIError


def groupfinder(username, request):
    user = get_user(username)
    if not user:
        users_group = get_group('user')
        new = Users(
            username=username,
            fullname=username,
            email="%s@example.com" % username
        )
        try:
            DBSession.add(new)
        except DBAPIError:
            raise

        newuser = get_user(username)
        print users_group.id
        member = Role_Membership(
            groupid=users_group.id,
            userid=newuser.id
        )
        try:
            DBSession.add(member)
        except DBAPIError:
            raise
    else:
        existing_user = get_user(username)
        return get_users_groups(existing_user.id)
