import os
import uuid
from hashlib import sha256

from cas import CASPrincipal
from nanohttp import context, settings, HTTPStatus
from restfulpy.orm import DeclarativeBase, Field, DBSession, relationship
from restfulpy.principal import JwtRefreshToken
from sqlalchemy import Unicode, Integer, JSON
from sqlalchemy.orm import synonym
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, \
    MagicAnalyzer, ContentTypeValidator
from sqlalchemy_media.constants import KB
from sqlalchemy_media.exceptions import DimensionValidationError, \
    AspectRatioValidationError, MaximumLengthIsReachedError, \
    ContentTypeValidationError

from ..cryptohelpers import OCRASuite, TimeBasedChallengeResponse,\
    derivate_seed
from ..oauth.scopes import SCOPES
from ..oauth.tokens import AccessToken
from .messaging import OTPSMS


AVATAR_CONTENT_TYPES = ['image/jpeg', 'image/png']
AVATAR_MAXIMUM_LENGTH = 50

class Avatar(Image):
    __pre_processors__ = [
        MagicAnalyzer(),
        ContentTypeValidator([
            'image/jpeg',
            'image/png',
        ]),
        ImageAnalyzer(),
        ImageValidator(
            minimum=(200, 200),
            maximum=(300, 300),
            min_aspect_ratio=1,
            max_aspect_ratio=1,
            content_types=AVATAR_CONTENT_TYPES
        ),
    ]

    __max_length__ = 50 * KB
    __min_length__ = AVATAR_CONTENT_TYPES * KB
    __prefix__ = 'avatar'


class Member(DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    email = Field(
        Unicode(100),
        unique=True,
        index=True,
        min_length=7,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        pattern_description='Invalid email format, example: user@example.com',
        python_type=str,
        not_none=True,
        required=True,
        watermark='user@example.com',
        example='user@example.com',
        label='Email Address',
        message='Enter your email address',
    )
    title = Field(
        Unicode(100),
        unique=True,
        pattern=r'^[a-zA-Z][\w]{5,19}$',
        pattern_description='Username can only include alphanumeric characters'
            'and underscore',
        python_type=str,
        not_none=True,
        required=True,
        min_length=6,
        max_length=20,
        example='John_Doe',
        watermark='John_Doe',
        label='Username',
        message='Enter your username',
    )
    name = Field(
        Unicode(20),
        nullable=True,
        not_none=False,
        python_type=str,
        min_length=3,
        max_length=20,
        required=False,
        pattern=r'^[a-zA-Z]{1}[a-z-A-Z ,.\'-]{2,19}$',
        pattern_description='Only alphabetical characters, ., \' and space are'
            'valid',
        example='John Doe',
        label='Full Name',
        watermark='John Doe',
        message='Enter your full name',
    )
    phone = Field(
        Unicode(16),
        nullable=True,
        not_none=False,
        unique=True,
        pattern=r'^[+]{0,1}[\d+]{7,15}$',
        pattern_description='Lorem ipsum dolor sit amet',
        python_type=str,
        required=False,
        min_length=8,
        max_length=16,
        watermark='Enter your phone number',
        label='Phone Number',
        example='+9891234567',
    )
    role = Field(Unicode(100))
    _avatar = Field(
        'avatar',
        Avatar.as_mutable(JSON),
        nullable=True,
        protected=False,
        json='avatar',
        not_none=False,
        label='Avatar',
        required=False,
    )
    _password = Field(
        'password',
        Unicode(128),
        index=True,
        protected=True,
        json='password',
        pattern=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+$',
        pattern_description='Password must include at least one uppercase, one'
            'lowercase and one number',
        example='ABCabc123',
        watermark='******',
        label='Password',
        message='Allowed special characters: !@#$%^&*)(><"',
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

    organizations = relationship(
        'Organization',
        back_populates='members',
        secondary='organization_member',
        protected=True,
    )


    @property
    def avatar(self):
        return self._avatar.locate() if self._avatar else None

    @avatar.setter
    def avatar(self, value):
        if value is not None:
            try:
                self._avatar = Avatar.create_from(value)

            except DimensionValidationError as e:
                raise HTTPStatus(f'618 {e}')

            except AspectRatioValidationError as e:
                raise HTTPStatus(
                    '619 Invalid aspect ratio Only 1/1 is accepted.'
                )

            except ContentTypeValidationError as e:
                raise HTTPStatus(f'620 {e}')

            except MaximumLengthIsReachedError as e:
                raise HTTPStatus(f'621 {e}')

        else:
            self._avatar = None

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
        return CASPrincipal({
            'id': self.id,
            'referenceId': self.id,
            'email': self.email,
            'name': self.name,
            'title': self.title,
            'avatar': self.avatar,
            'roles': [self.role],
            'sessionId': str(uuid.uuid4()),
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
            result = super().to_dict()
            result['avatar'] = self.avatar
            return result

        member = dict.fromkeys(SCOPES.keys(), None)
        member['id'] = self.id
        if context.identity.scopes is None:
            return member

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
            ocra_suite,
            derivate_seed(seed, str(phone))
        )

    @classmethod
    def generate_activation_code(cls, phone, id):
        session = cls._create_activation_session(phone)
        return session.generate(challenge=id)

    @classmethod
    def verify_activation_code(cls, phone, id, code):
        session = cls._create_activation_session(phone)
        result, ___ = session.verify(
            code,
            str(id),
            settings.phone.activation_code.window
        )
        return result

    @classmethod
    def create_otp(cls, phone, id):
        return OTPSMS(
            receiver=phone,
            code=cls.generate_activation_code(phone, str(id))
        )

    def __repr__(self):
        return f'Member: {self.id} {self.title} {self.email}'

