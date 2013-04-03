from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import groupfinder
from .models import DBSession


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', callback=groupfinder)
    authz_policy = ACLAuthorizationPolicy()

    session_factory = session_factory = session_factory_from_settings(settings)

    config = Configurator(settings=settings,
                          root_factory='.models.RootFactory',
                          session_factory=session_factory)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # Routes
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home_page', '/')

    # Admin
    config.add_route('admin_list_users', '/admin/users')
    config.add_route('admin_list_teams', '/admin/teams')

    config.scan()
    return config.make_wsgi_app()
