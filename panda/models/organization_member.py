from restfulpy.orm import Field, PaginationMixin, FilteringMixin, \
    OrderingMixin, BaseModel, ModifiedMixin, TimestampMixin, relationship
from sqlalchemy import Integer, Unicode, select, and_, FLOAT, or_, ARRAY
from sqlalchemy.orm import mapper

from . import Organization, OrganizationMember, Member


class AbstractOrganizationMember(PaginationMixin, OrderingMixin, \
                                 FilteringMixin, ModifiedMixin, \
                                 TimestampMixin, BaseModel):
    __abstract__ = True
    __table_args__ = {'autoload': True}

    id = Field('id', Integer, primary_key=True)
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

    members = Field('members', ARRAY(Member), default=[])

    @classmethod
    def create_mapped_class(cls):
        columns = [
            Organization.id,
            Organization.title,
            Organization.domain,
            Organization.url,
            Organization.members,
        ]


        query = select(columns).select_from(Organization)

        class OraganizationMember(cls):
           pass

        mapper(OraganizationMember, query.alias())
        return OraganizationMember

