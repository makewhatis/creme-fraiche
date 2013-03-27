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

from ..models import DBSession


@view_config(
    route_name='home_page',
    renderer='/home/index.mak'
)
def home_page(request):
    return {'project': 'creme fraiche'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_creme_fraiche_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

