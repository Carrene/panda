from nanohttp import HTTPStatus
from restfulpy.orm import DeclarativeBase, Field, relationship, \
    ModifiedMixin, TimestampMixin
from sqlalchemy import Unicode, Integer, ForeignKey, Enum, JSON
from sqlalchemy_media import Image, ImageAnalyzer, ImageValidator, \
    MagicAnalyzer, ContentTypeValidator
from sqlalchemy_media.constants import KB
from sqlalchemy_media.exceptions import DimensionValidationError, \
    AspectRatioValidationError, MaximumLengthIsReachedError, \
    ContentTypeValidationError


roles = [
    'owner',
    'member',
]


class OrganizationMember(DeclarativeBase):
    __tablename__ = 'organization_member'

    member_id = Field(Integer, ForeignKey('member.id'), primary_key=True)
    organization_id = Field(
        Integer,
        ForeignKey('organization.id'),
        primary_key=True
    )
    role = Field(
        Enum(*roles, name='roles'),
        python_type=str,
        label='role',
        watermark='Choose a roles',
        not_none=True,
        required=True,
        default='owner'
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


class Organization(ModifiedMixin, TimestampMixin, DeclarativeBase):
    __tablename__ = 'organization'

    id = Field(Integer, primary_key=True)

    title = Field(
        Unicode(40),
        unique=True,
        index=True,
        min_length=1,
        max_length=40,
        pattern=r'^([0-9a-zA-Z]+-?[0-9a-zA-Z]*)*[\da-zA-Z]$',
        pattern_description='Lorem ipsum dolor sit amet',
        python_type=str,
        not_none=True,
        required=True,
        watermark='Enter your organization name',
        example='netalic',
        label='Name',
    )

    url = Field(
        Unicode(50),
        pattern=r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www.)+'
            r'[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\.*)?$',
        pattern_description='Lorem ipsum dolor sit amet',
        min_length=1,
        max_length=50,
        python_type=str,
        required=False,
        nullable=True,
        not_none=False,
        watermark='Enter your URL',
        example='www.example.com',
        label='URL',
    )

    domain = Field(
        Unicode(50),
        pattern=r'^[^www.][a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]'
            r'{2,5}(:[0-9]{1,5})?$',
        pattern_description='Lorem ipsum dolor sit amet',
        min_length=1,
        max_length=50,
        python_type=str,
        required=False,
        nullable=True,
        not_none=False,
        watermark='Enter your domain',
        example='example.com',
        label='Domain',
    )

    _icon = Field(
        'icon',
        Icon.as_mutable(JSON),
        nullable=True,
        not_none=False,
        required=False,
        label='Icon',
        protected=False,
        json='icon',
    )

    members = relationship(
        'Member',
        secondary='organization_member',
        lazy='selectin',
        back_populates='organizations',
        protected=True
    )

    @property
    def icon(self):
        return self._icon.locate() if self._icon else None

    @icon.setter
    def icon(self, value):
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

    def to_dict(self):
        organization = super().to_dict()
        organization['icon'] = self.icon
        return organization

