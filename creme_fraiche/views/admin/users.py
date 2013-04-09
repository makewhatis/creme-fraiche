from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from creme_fraiche.models import DBSession
from creme_fraiche.models import Users

from pyramid.httpexceptions import HTTPFound

import logging


@view_config(
    route_name='admin_list_users',
    renderer='/admin/users/list.mak',
    permission='admin'
)
def admin_list_users(request):
    users = DBSession.query(Users).all()
    print users
    for user in users:
        print user
    return dict(
        project='creme fraiche',
        users=users,
        logged_in=authenticated_userid(request)
    )


@view_config(
    route_name='admin_create_user',
    request_method="GET",
    renderer='/admin/users/create.mak',
    permission='admin'
)
def admin_create_user(request):
    users = DBSession.query(Users).all()

    return dict(
        project='creme fraiche',
        users=users,
        logged_in=authenticated_userid(request)
    )

@view_config(
    route_name='admin_create_user',
    request_method="POST",
    permission='admin'
)
def admin_create_user_post(request):
    username = request.POST.get('username')
    fullname = request.POST.get('fullname')
    email = request.POST.get('email')

    try:
        users = Users.create(username, fullname, email)
    except Exception as e:
        logging.error(e)
        request.session.flash(e.message, 'warning')
        return HTTPFound(
            location=request.route_url(
                'admin_create_user'
            )
        )

    request.session.flash("User Created.", 'success')
    return HTTPFound(location=request.route_url('admin_list_users'))