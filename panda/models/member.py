import os
from hashlib import sha256

from nanohttp import context
from restfulpy.orm import DeclarativeBase, Field, DBSession, relationship
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from sqlalchemy import Unicode, Integer
from sqlalchemy.orm import synonym

from ..oauth.scopes import SCOPES
from ..oauth.tokens import AccessToken


class Member(DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        pattern='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        required=True
    )
    title = Field(
        Unicode(100),
        unique=True,
        pattern='^[a-zA-Z][\w]{5,19}$',
        required=True,
        min_length=6,
        max_length=20
    )
    role = Field(Unicode(100))
    _password = Field(
        'password',
        Unicode(128),
        index=True,
        protected=True,
        pattern='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+',
        min_length=6,
        max_length=20,
        required=True
    )
    applications = relationship(
        'Application',
        back_populates='owner',
        protected=True
    )

    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hashed_pass = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hashed_pass.update((password + salt).encode('utf-8'))
        hashed_pass = hashed_pass.hexdigest()

        password = salt + hashed_pass
        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym(
        '_password',
        descriptor=property(_get_password, _set_password),
        info=dict(protected=True)
    )

    def create_jwt_principal(self):
        return JwtPrincipal({
            'id': self.id,
            'email': self.email,
            'name': self.title,
            'roles': [self.role]
        })

    def create_refresh_principal(self):
        return JwtRefreshToken(dict(id=self.id))

    def validate_password(self, password):
        hashed_pass = sha256()
        hashed_pass.update((password + self.password[:64]).encode('utf-8'))

        return self.password[64:] == hashed_pass.hexdigest()

    @classmethod
    def current(cls):
        return DBSession.query(cls) \
            .filter(cls.email == context.identity.email) \
            .one()

    def to_dict(self):
        if not isinstance(context.identity, AccessToken):
            return super().to_dict()

        member = dict.fromkeys(SCOPES.keys(), None)
        member['id'] = self.id
        for scope in context.identity.scopes:
            member[scope] = SCOPES[scope](self)

        return member

