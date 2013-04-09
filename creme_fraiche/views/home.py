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
from creme_fraiche.models import authenticate

from creme_fraiche.exceptions import AuthException

import logging
log = logging.getLogger(__name__)

@view_config(
    route_name='home_page',
    renderer='/home/index.mak'
)
def home_page(request):

    try:
        users = DBSession.query(Users).all()
    except DBAPIError as e:
        print(e)

    return dict(
        project='creme fraiche',
        users=users,
        logged_in=authenticated_userid(request)
    )


@view_config(
    context=Exception,
    renderer='/home/fail.mak'
)
def fail_view(exc, request):
    log.exception(exc)
    msg="Uh oh. Somethings broke."
    return dict(
        msg=msg,
        project='creme_fraiche'
    )


@view_config(
    route_name='login',
    renderer='/home/login.mak'
)
@forbidden_view_config(renderer='/home/login.mak')
def login_view(request):
    login_url = request.route_url('login')
    referrer = request.url
    print "URL: %s" % referrer
    if referrer == login_url:
        referrer = '/'  # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)

    message = ''
    login = ''
    password = ''
    if request.POST:
        login = request.POST.get('username')
        password = request.POST.get('password')

        try:
            userobj = authenticate(login, password)
        except AuthException as e:
            userobj = False
        
        if userobj:
            headers = remember(request, login)
            request.session.flash("Logged in successfully!", 'success')
            return HTTPFound(location=came_from, headers=headers)
        else:
            request.session.flash("Login Failed.", 'warning')
            return HTTPFound(location=request.route_url('login', message='done'))

    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
        logged_in=authenticated_userid(request)
    )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    request.session.delete()
    return HTTPFound(location=request.route_url('home_page'),
                     headers=headers)

