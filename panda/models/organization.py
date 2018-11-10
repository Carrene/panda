from restfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Unicode, Integer, ForeignKey, Enum


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


class Organization(DeclarativeBase):
    __tablename__ = 'organization'

    id = Field(Integer, primary_key=True)
    name = Field(
        Unicode(40),
        unique=True,
        index=True,
        min_length=1,
        max_length=40,
        pattern=r'^([0-9a-zA-Z]+-?[0-9a-zA-Z]*)*[^-]$',
        pattern_description='Lorem ipsum dolor sit amet',
        python_type=str,
        not_none=True,
        required=True,
        watermark='Enter your organization name',
        example='netalic',
        label='Name',
    )

    members = relationship(
        'Member',
        secondary='organization_member',
        lazy='selectin',
        back_populates='organizations',
        protected=True
    )

