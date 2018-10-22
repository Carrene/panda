import os
from hashlib import sha256

from nanohttp import context, settings, HTTPStatus
from restfulpy.orm import DeclarativeBase, Field, DBSession, relationship
from restfulpy.principal import JwtPrincipal, JwtRefreshToken
from sqlalchemy import Unicode, Integer, JSON
from sqlalchemy.orm import synonym
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, \
    MagicAnalyzer, ContentTypeValidator
from sqlalchemy_media.constants import KB
from sqlalchemy_media.exceptions import DimensionValidationError, \
    AspectRatioValidationError, MaximumLengthIsReachedError, \
    ContentTypeValidationError, ImageProcessor
from sqlalchemy_media.constants import KB
from sqlalchemy_media.exceptions import DimensionValidationError, \
    AspectRatioValidationError, AnalyzeError, MaximumLengthIsReachedError

from ..cryptohelpers import OCRASuite, TimeBasedChallengeResponse,\
    derivate_seed
from ..oauth.scopes import SCOPES
from ..oauth.tokens import AccessToken
from .messaging import OTPSMS


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
            content_types=['image/jpeg', 'image/png']
        ),
    ]

    __max_length__ = 50 * KB
    __min_length__ = 1 * KB
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
        python_type=str,
        not_none=True,
        required=True,
        watermark='Enter your email address',
        example='user@example.com',
        label='Email Address',
    )
    title = Field(
        Unicode(100),
        unique=True,
        pattern=r'^[a-zA-Z][\w]{5,19}$',
        python_type=str,
        not_none=True,
        required=True,
        min_length=6,
        max_length=20,
        example='user',
        watermark='Enter your username',
        label='Username',
    )
    name = Field(
        Unicode(20),
        nullable=True,
        python_type=str,
        min_length=3,
        max_length=20,
        required=False,
        pattern=r'^[a-zA-Z]{1}[a-z-A-Z ,.\'-]{2,19}$',
        example='User',
        label='Name',
        watermark='Enter your name',
    )
    phone = Field(
        Unicode(16),
        nullable=True,
        unique=True,
        pattern=r'^[+]{0,1}[\d+]{7,15}$',
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
        example='123abcABC',
        watermark='Enter your password',
        label='Password',
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
                raise HTTPStatus(f'619 {e}')

            except ContentTypeValidationError as e:
                raise HTTPStatus(f'620 {e}')

            except AnalyzeError as e:
                raise HTTPStatus(f'620 {e}')

            except MaximumLengthIsReachedError as e:
                raise HTTPStatus(f'621 {e}')
            except FileNotFoundError as e:
                raise HTTPStatus(f'622 No Such File Or Directory')

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
            result = super().to_dict()
            result['avatar'] = self.avatar
            return result

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

