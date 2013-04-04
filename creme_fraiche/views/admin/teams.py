from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from creme_fraiche.models import DBSession
from creme_fraiche.models import Teams


@view_config(
    route_name='admin_list_teams',
    renderer='/admin/teams/list.mak',
    permission='admin'
)
def admin_list_teams(request):
    teams = DBSession.query(Teams).all()

    return dict(
        project='creme fraiche',
        teams=teams,
        logged_in=authenticated_userid(request)
    )
