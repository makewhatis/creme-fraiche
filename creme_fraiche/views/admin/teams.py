from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid

from sqlalchemy import desc
from sqlalchemy.exc import DBAPIError

from creme_fraiche.models import DBSession
from creme_fraiche.models import Teams

from pyramid.httpexceptions import HTTPFound

import logging


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


@view_config(
    route_name='admin_create_team',
    request_method="GET",
    renderer='/admin/teams/create.mak',
    permission='admin'
)
def admin_create_team(request):
    teams = DBSession.query(Teams).all()

    return dict(
        project='creme fraiche',
        teams=teams,
        logged_in=authenticated_userid(request)
    )


@view_config(
    route_name='admin_create_team',
    request_method="POST",
    permission='admin'
)
def admin_create_team_post(request):
    teamname = request.POST.get('teamname')

    try:
        team = Teams.create(teamname)
    except Exception as e:
        logging.error(e)
        request.session.flash(e.message, 'warning')
        return HTTPFound(
            location=request.route_url(
                'admin_create_team'
            )
        )

    request.session.flash("Team Created.", 'success')
    return HTTPFound(location=request.route_url('admin_list_teams'))


@view_config(
    route_name='admin_delete_team',
    request_method="GET",
    permission='admin'
)
def admin_delete_team(request):
    team = DBSession.query(Teams)\
        .filter(Teams.id == request.matchdict.get('id'))\
        .first()

    try:
        DBSession.delete(team)
    except Exception as e:
        logging.error(e)
        request.session.flash(e.message, 'warning')
        return HTTPFound(
            location=request.route_url(
                'admin_create_team'
            )
        )
    request.session.flash("Team Deleted.", 'success')
    return HTTPFound(
        location=request.route_url(
            'admin_list_teams'
        )
    )
