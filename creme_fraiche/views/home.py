from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import forbidden_view_config
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.security import forget

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from creme_fraiche.models import DBSession
from creme_fraiche.models import Users


@view_config(
    route_name='home_page',
    renderer='/home/index.mak'
)
def home_page(request):

    users = DBSession.query(Users).all()
    return dict(
        project='creme fraiche',
        users=users
    )


@view_config(
    context=Exception,
    renderer='/home/fail.mak'
)
def fail_view(exc, request):
    msg="Uh oh. Somethings broke."
    return dict(
        msg=msg,
        project='creme_fraiche'
    )

