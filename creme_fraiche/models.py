import sys
import ldap
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
               (Allow, 'admins', 'admin'),
               (Allow, 'admins', 'user'),
               (Allow, 'users', 'user')]

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


# very temporary
config = {
    'ldap_url': 'ldap_url',
    'userdn': 'userdn',
    'password': 'password',
    'bind_dn': 'bind_dn'
}


def authenticate(username, password):
    con = ldap.initialize(config['ldap_url'])
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    user_dn = config['userdn']
    user_pw = config['password']
    # development setting
    return True

    try:
        # Perform bind to lookup user
        con.simple_bind_s(user_dn, user_pw)
        user_info = con.search_s(
            config['bind_dn'],
            ldap.SCOPE_SUBTREE,
            '(mail=%s@example.com)' % username,
            ['cn', 'mail']
        )
        # Assign userDN to uname
        if user_info == []:
            log.info("%s not found." % username)
            return False

        uname = user_info[0][0]
        log.debug("LDAP Username: %s " % uname)
        #Simple bind
        con.simple_bind_s(uname, password)
        return True
    except ldap.LDAPError, e:
        log.info("LDAP Login failed for %s" % (uname))


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


def get_users_groups(user_id):
    try:
        groupsobj = DBSession.query(Group).filter(
            Group.id == Membership.groupid).\
            filter(Membership.userid == user_id)
    except DBAPIError:
        raise
    groups = []
    for group in groupsobj:
        if group.shortname == 'role':
            groups.append(group.name)
    return groups


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
