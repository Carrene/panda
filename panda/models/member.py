import os
from hashlib import sha256

from nanohttp import context, settings
from restfulpy.orm import DeclarativeBase, Field, DBSession, relationship
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from sqlalchemy import Unicode, Integer
from sqlalchemy.orm import synonym

from ..cryptohelpers import OCRASuite, TimeBasedChallengeResponse,\
    derivate_seed
from ..oauth.scopes import SCOPES
from ..oauth.tokens import AccessToken
from .messaging import OTPSMS


class Member(DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        min_length=7,
        max_length=100,
        pattern='(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        python_type=str,
        not_none=True,
        required=True,
        watermark='Enter your email address',
        example='user@example.com',
        label='Email Address',
        name='Email',
    )
    title = Field(
        Unicode(100),
        unique=True,
        pattern='^[a-zA-Z][\w]{5,19}$',
        python_type=str,
        not_none=True,
        required=True,
        min_length=6,
        max_length=20,
        example='user',
        watermark='Enter your title',
        label='Title',
    )
    name = Field(
        Unicode(20),
        nullable=True,
        python_type=str,
        min_length=3,
        max_length=20,
        required=False,
        pattern='^[a-zA-Z]{1}[a-z-A-Z ,.\'-]{2,19}$',
        example='User name',
        label='Name',
        watermark='Enter your name',
    )
    phone = Field(
        Unicode(16),
        nullable=True,
        unique=True,
        pattern='^[+]{0,1}[\d+]{7,15}$',
        python_type=str,
        required=False,
        min_length=8,
        max_length=16,
        watermark='Enter your phone number',
        label='Phone Number',
        example='+9891234567',
    )
    role = Field(Unicode(100))
    _password = Field(
        'password',
        Unicode(128),
        index=True,
        protected=True,
        json='password',
        pattern='(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+',
        example='123abcABC',
        watermark='Enter your password',
        label='password',
        min_length=6,
        max_length=20,
        required=True,
        python_type=str,
        not_none=True,
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

    @classmethod
    def _create_activation_session(cls, phone):
        ocra_suite = OCRASuite(
            'time',
            settings.phone.activation_code.length,
            settings.phone.activation_code.hash_algorithm,
            settings.phone.activation_code.time_interval,
            settings.phone.activation_code.challenge_limit
        )
        seed = settings.phone.activation_code.seed
        return TimeBasedChallengeResponse(
            ocra_suite, derivate_seed(seed, str(phone))
        )

    @classmethod
    def generate_activation_code(cls, phone, id):
        session = cls._create_activation_session(phone)
        return session.generate(challenge=id)

    @classmethod
    def verify_activation_code(cls, phone, id, code):
        session = cls._create_activation_session(phone)
        result, ___ = session.verify(
            code, str(id), settings.phone.activation_code.window
        )
        return result

    @classmethod
    def create_otp(cls, phone, id):
        return OTPSMS(
            receiver=phone, code=cls.generate_activation_code(phone, str(id))
        )

