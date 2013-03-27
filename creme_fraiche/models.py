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


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    name = Column(String(50))
    email = Column(String(50))

    groups = association_proxy(
        "user_associations", "group")

    def __init__(self, username, name, email):
        self.username = username
        self.name = name
        self.email = email

    @classmethod
    def get_by_username(cls, username):
        return DBSession.query(cls).filter(cls.username == username).first()

    @classmethod
    def check_password(cls, username, password):
        user = cls.authenticate(username, password)
        if not user:
            return False
        return user


class Group(Base):

    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    shortname = Column(Unicode(50))
    status = Column(Integer)

    def __init__(self, name, shortname, status):
        self.name = name
        self.shortname = shortname
        self.status = status

    def __repr__(self):
        return 'Group(%s)' % repr(self.name)


class Membership(Base):

    __tablename__ = 'membership'
    userid = Column(Integer, ForeignKey('user.id'), primary_key=True)
    groupid = Column(Integer, ForeignKey('group.id'), primary_key=True)

    user = relationship(
        User,
        backref=backref(
            "user_associations",
            cascade="all, delete-orphan"
        )
    )

    group = relationship("Group")

    def __init__(self, userid, groupid):
        self.userid = userid
        self.groupid = groupid

# very temporary
config = {
    'ldap_url' = 'ldap_url',
    'userdn' = 'userdn',
    'password' = 'password',
    'bind_dn' = 'bind_dn'
}


def authenticate(username, password):
    con = ldap.initialize(config['ldap_url'])
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    user_dn = config['userdn']
    user_pw = config['password']
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


def get_group(group):
    try:
        group = DBSession.query(Group).filter(Group.name == str(group)).first()
    except DBAPIError:
        raise
    return group


def get_user(username):
    try:
        user = DBSession.query(User).filter(
            User.username == str(username)).first()
    except DBAPIError:
        raise
    return user


def get_user_by_id(userid):
    try:
        user = DBSession.query(User).filter(User.id == userid).first()
    except DBAPIError:
        raise
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
