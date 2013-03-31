import os
import sys
from pkg_resources import resource_filename

ROOT_PATH = os.path.dirname(__file__)


def pytest_sessionstart():
    from py.test import config
    from pyramid.config import Configurator
    from creme_fraiche.models import Base
    from creme_fraiche.models import insert_base
    from paste.deploy.loadwsgi import appconfig
    from sqlalchemy import engine_from_config
    import os

    ROOT_PATH = os.path.dirname(__file__)
    settings = appconfig(
        'config:' + resource_filename(
            __name__,
            'creme_fraiche/tests/test.ini'
        )
    )

    engine = engine_from_config(settings, prefix='sqlalchemy.')

    print('Creating the tables on the test database %s' % engine)

    config = Configurator(settings=settings)
    config.scan('creme_fraiche.models')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    insert_base(engine)
