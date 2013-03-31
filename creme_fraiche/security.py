from .models import get_role
from .models import get_user_by_username
from .models import get_users_groups
from .models import DBSession
from .models import Users
from .models import Role_Membership
from sqlalchemy.exc import DBAPIError


def groupfinder(username, request):
    user = get_user_by_username(username)
    if not user:
        user_role = get_role('user')
        new = Users(
            username=username,
            fullname=username,
            email="%s@example.com" % username
        )
        try:
            DBSession.add(new)
        except DBAPIError:
            raise

        newuser = get_user_by_username(username)
        print user_role.id
        member = Role_Membership(
            groupid=user_role.id,
            userid=newuser.id
        )
        try:
            DBSession.add(member)
        except DBAPIError:
            raise
    else:
        existing_user = get_user_by_username(username)
        return get_users_groups(existing_user.id)
