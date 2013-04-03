from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from creme_fraiche.models import DBSession
from creme_fraiche.models import Users


@view_config(
    route_name='admin_list_users',
    renderer='/admin/users/list.mak'
)
def admin_list_users(request):
    users = DBSession.query(Users).all()
    print users
    for user in users:
        print user
    return dict(
        project='creme fraiche',
        users=users
    )


@view_config(
    route_name='admin_create_user',
    request_method="GET",
    renderer='/admin/users/create.mak'
)
def admin_create_user(request):
    users = DBSession.query(Users).all()
    print users
    for user in users:
        print user
    return dict(
        project='creme fraiche',
        users=users
    )

@view_config(
    route_name='admin_create_user',
    request_method="POST"
)
def admin_create_user_post(request):
    users = DBSession.query(Users).all()
    print users
    for user in users:
        print user
    return dict(
        project='creme fraiche',
        users=users
    )