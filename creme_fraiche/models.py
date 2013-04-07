import sys
import re
import time
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.types import DateTime
from sqlalchemy.types import Unicode
from sqlalchemy.types import Boolean

from sqlalchemy import func
from sqlalchemy.exc import DBAPIError

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from zope.sqlalchemy import ZopeTransactionExtension

import transaction

from pyramid.security import Allow
from pyramid.security import Everyone

from creme_fraiche.exceptions import AuthException

import logging
log = logging.getLogger(__name__)

DBSession = scoped_session(
    sessionmaker(
        extension=ZopeTransactionExtension()
    )
)

Base = declarative_base()


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'admin', 'admin'),
               (Allow, 'admin', 'user'),
               (Allow, 'user', 'user')]

    def __init__(self, request):
        pass


class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    fullname = Column(String(150))
    email = Column(String(50))

    roles = association_proxy(
        "role_associations", "roles")

    teams = association_proxy(
        "team_associations", "teams")

    def __init__(
        self,
        username,
        fullname,
        email
    ):
        self.username = username
        self.fullname = fullname
        self.email = email

    def __repr__(self):
        return 'Users(%s)' % repr(self.username)

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.authenticate(username, password)
        if not user:
            return False
        return user


class Roles(Base):

    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    def __init__(
        self,
        name
    ):
        self.name = name

    def __repr__(self):
        return 'Roles(%s)' % repr(self.name)


class Teams(Base):

    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    def __init__(
        self,
        name
    ):
        self.name = name

    def __repr__(self):
        return 'Teams(%s)' % repr(self.name)


class Team_Membership(Base):

    __tablename__ = 'team_membership'
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )
    team_id = Column(
        Integer,
        ForeignKey('teams.id'),
        primary_key=True
    )

    user = relationship(
        Users,
        backref=backref(
            "team_associations",
            cascade="all, delete-orphan"
        )
    )

    team = relationship("Teams")

    def __init__(
        self,
        user_id,
        team_id
    ):
        self.user_id = user_id
        self.team_id = team_id


class Role_Membership(Base):

    __tablename__ = 'role_membership'
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )
    role_id = Column(
        Integer,
        ForeignKey('roles.id'),
        primary_key=True
    )

    user = relationship(
        Users,
        backref=backref(
            "role_associations",
            cascade="all, delete-orphan"
        )
    )

    role = relationship("Roles")

    def __init__(
        self,
        user_id,
        role_id
    ):
        self.user_id = user_id
        self.role_id = role_id


class ReportFormats(Base):

    __tablename__ = 'report_formats'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))

    def __init__(
        self,
        name
    ):
        self.name = name

    def __repr__(self):
        return 'ReportFormats(%s)' % repr(self.name)


class ReportTemplates(Base):

    __tablename__ = 'report_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    style = Column(Text)

    def __init__(
        self,
        name,
        style
    ):
        self.name = name
        self.style = style

    def __repr__(self):
        return 'ReportTemplates(%s)' % repr(self.name)


class Reports(Base):

    __tablename__ = 'reports'
    id = Column(
        Integer,
        primary_key=True
    )
    team_id = Column(
        Integer,
        ForeignKey('teams.id')
    )
    template_id = Column(
        Integer,
        ForeignKey('report_templates.id')
    )
    format_id = Column(
        Integer,
        ForeignKey('report_formats.id')
    )
    report_time = Column(
        DateTime,
        default=func.now()
    )

    def __init__(
        self,
        team_id,
        template_id,
        format_id,
        report_time=func.now()
    ):
        self.team_id = team_id
        self.template_id = template_id
        self.format_id = format_id
        self.report_time = report_time


class PermissionTypes(Base):

    __tablename__ = 'permission_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))

    def __init__(
        self,
        name
    ):
        self.name = name

    def __repr__(self):
        return 'PermissionTypes(%s)' % repr(self.name)


class TemplatePermissions(Base):

    __tablename__ = 'template_permissions'

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey('users.id')
    )
    template_id = Column(
        Integer,
        ForeignKey('report_templates.id')
    )
    permission_id = Column(
        Integer,
        ForeignKey('permission_types.id')
    )

    def __init__(
        self,
        user_id,
        template_id,
        permission_id
    ):
        self.user_id = user_id
        self.template_id = template_id
        self.permission_id = permission_id


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(50))
    parent_id = Column(Integer)
    team_id = Column(
        Integer,
        ForeignKey('teams.id')
    )

    def __init__(
        self,
        name,
        team_id,
        parent_id=None,
    ):
        self.name = name
        self.team_id = team_id
        self.parent_id = parent_id

    def __repr__(self):
        return 'Category(%s)' % self.name


class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True, unique=True)
    data = Column(Text)
    user_id = Column(
        Integer,
        ForeignKey('users.id')
    )
    cat_id = Column(
        Integer,
        ForeignKey('category.id')
    )
    team_id = Column(
        Integer,
        ForeignKey('teams.id')
    )
    entry_time = Column(
        DateTime,
        default=func.now()
    )

    def __init__(
        self,
        data,
        user_id,
        cat_id,
        team_id,
        entry_time=func.now()
    ):
        self.data = data
        self.user_id = user_id
        self.cat_id = cat_id
        self.team_id = team_id
        self.entry_time = entry_time

    def __repr__(self):
        return 'Entry(%s)' % self.data


def authenticate(username, password):
    # during development
    if username == 'admin':
        if password == 'letmein':
            return True
        else:
            raise AuthException
    else:
        return False


def get_team(team):
    try:
        result = DBSession.query(Teams).filter(Teams.name == str(team)).first()
    except DBAPIError:
        log.error("Error querying team: %s" % team)
        return False
    return result


def get_role(role):
    try:
        result = DBSession.query(Roles).filter(Roles.name == str(role)).first()
    except DBAPIError:
        log.error("Error querying role: %s" % role)
        return False
    return result


def get_user_by_username(username):
    try:
        user = DBSession.query(Users).filter(
            Users.username == str(username)).first()
    except DBAPIError:
        log.error("Error querying user: %s" % username)
        return False
    return user


def get_user_by_id(user_id):
    try:
        user = DBSession.query(Users).filter(Users.id == user_id).first()
    except DBAPIError:
        log.error("Error querying user: %s" % user_id)
        return False
    return user


def get_users_roles(user_id):
    try:
        roles_obj = DBSession.query(Roles).filter(
            Roles.id == Role_Membership.role_id).\
            filter(Role_Membership.user_id == user_id).all()
    except DBAPIError:
        log.error("Error querying roles for: %s" % user_id)
        return False

    roles = []
    for role in roles_obj:
        roles.append(role.name)
    return roles


def insert_base(eng):
    # create a Session
    DBSession.configure(bind=eng)
    with transaction.manager:
        users = [
            Users(
                "admin",
                "MF Jones",
                "admin@localhost"
            ),
        ]
        DBSession.add_all(users)
        transaction.manager.commit()

        new_roles = [
            Roles('admin'),
            Roles('user'),
        ]
        DBSession.add_all(new_roles)
        transaction.manager.commit()

        new_teams = [
            Teams('Linux'),
            Teams('Accounting')
        ]

        DBSession.add_all(new_teams)
        transaction.manager.commit()

        new_team_members = [
            Team_Membership(1, 1),
            Team_Membership(1, 2)
        ]

        DBSession.add_all(new_team_members)
        transaction.manager.commit()

        new_role_members = [
            Role_Membership(1, 1),
            Role_Membership(1, 2)
        ]

        DBSession.add_all(new_role_members)
        transaction.manager.commit()

        formats = [
            ReportFormats('html'),
            ReportFormats('pdf'),
            ReportFormats('text')
        ]
        DBSession.add_all(formats)
        transaction.manager.commit()

        templates = [
            ReportTemplates('ops', ".clearfix {*zoom: 1;]"),
            ReportTemplates('dev', ".clearfix {*zoom: 2;]")
        ]
        DBSession.add_all(templates)
        transaction.manager.commit()

        reports = [
            Reports(1, 1, 1),
            Reports(1, 2, 2)
        ]
        DBSession.add_all(reports)
        transaction.manager.commit()

        permission_types = [
            PermissionTypes('read'),
            PermissionTypes('write'),
            PermissionTypes('none'),
        ]
        DBSession.add_all(permission_types)
        transaction.manager.commit()

        template_permissions = [
            TemplatePermissions(1, 1, 2),
            TemplatePermissions(1, 2, 1)
        ]
        DBSession.add_all(template_permissions)
        transaction.manager.commit()

        categories = [
            Category('Incidents', 1, None),
            Category('Changes', 1, None),
            Category('Projects', 1, None),
            Category('Patching', 1, 3)
        ]
        DBSession.add_all(categories)
        transaction.manager.commit()

        entries = [
            Entry('test incident', 1, 1, 1),
            Entry('test Patching', 1, 4, 1),
            Entry('test change', 1, 2, 1)
        ]
        DBSession.add_all(entries)
        transaction.manager.commit()
