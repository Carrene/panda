import base64

from nanohttp import context, HTTPStatus
from restfulpy.orm import DeclarativeBase, OrderingMixin, PaginationMixin, \
    FilteringMixin, Field, relationship
from sqlalchemy import Unicode, Integer, LargeBinary, ForeignKey, JSON
from sqlalchemy.orm import synonym
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, \
    MagicAnalyzer, ContentTypeValidator
from sqlalchemy_media.constants import KB
from sqlalchemy_media.exceptions import DimensionValidationError, \
    AspectRatioValidationError, MaximumLengthIsReachedError, \
    ContentTypeValidationError


class ApplicationMember(DeclarativeBase):
     __tablename__ = 'application_member'

     member_id = Field(Integer, ForeignKey('member.id'), primary_key=True)
     application_id = Field(
         Integer,
         ForeignKey('application.id'),
         primary_key=True
     )


class Icon(Image):
    __pre_processors__ = [
        MagicAnalyzer(),
        ContentTypeValidator([
            'image/jpeg',
            'image/png',
        ]),
        ImageAnalyzer(),
        ImageValidator(
            minimum=(100, 100),
            maximum=(200, 200),
            min_aspect_ratio=1,
            max_aspect_ratio=1,
            content_types=['image/jpeg', 'image/png']
        ),
    ]

    __max_length__ = 50 * KB
    __min_length__ = 1 * KB
    __prefix__ = 'icon'


class Application(DeclarativeBase, OrderingMixin, PaginationMixin,
                  FilteringMixin):
    __tablename__ = 'application'

    id = Field(Integer, primary_key=True)

    owner_id = Field(Integer, ForeignKey('member.id'))

    title = Field(
        Unicode(100),
        required=True,
        not_none=True,
        python_type=str,
        label='Title',
        min_length=1,
        max_length=100,
        watermark='Enter your title'
    )
    redirect_uri = Field(
        Unicode(100),
        required=True,
        not_none=True,
        label='Redirect Uri',
        min_length=1,
        max_length=100,
        python_type=str,
        watermark='Enter your redirect uri'
    )
    secret = Field(LargeBinary(32))
    _icon = Field(
        'icon',
        Icon.as_mutable(JSON),
        nullable=True,
    )

    owner = relationship(
        'Member',
        back_populates='applications',
        protected=True
    )

    members = relationship(
        'Member',
        secondary='application_member',
        lazy='selectin',
    )

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            redirectUri=self.safe_redirect_uri,
            ownerId=self.safe_owner_id,
            secret=self.safe_secret,
            icon=self.icon,
        )

    def validate_secret(self, secret):
        try:
            return self.secret == base64.decodebytes(bytes(secret, 'utf-8'))
        except:
            return False

    def am_i_owner(self):
        return context.identity and self.owner_id == context.identity.id

    @property
    def safe_secret(self):
        return base64.encodebytes(self.secret) if self.am_i_owner() else None

    @property
    def safe_redirect_uri(self):
        return self.redirect_uri if self.am_i_owner() else None

    @property
    def safe_owner_id(self):
        return self.owner_id if self.am_i_owner() else None

    def _get_icon(self):
        return self._icon.locate() if self._icon else None

    def _set_icon(self, value):
        if value is not None:
            try:
                self._icon = Icon.create_from(value)

            except DimensionValidationError as e:
                raise HTTPStatus(f'618 {e}')

            except AspectRatioValidationError as e:
                raise HTTPStatus(f'619 {e}')

            except ContentTypeValidationError as e:
                raise HTTPStatus(f'620 {e}')

            except MaximumLengthIsReachedError as e:
                raise HTTPStatus(f'621 {e}')

        else:
            self._icon = None

    icon = synonym(
        '_icon',
        descriptor=property(_get_icon, _set_icon),
        info=dict(protected=False, json='icon'),
    )

