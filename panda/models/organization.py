from restfulpy.orm import DeclarativeBase, Field
from sqlalchemy import Unicode, Integer


class Organization(DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)
    name = Field(
        Unicode(40),
        unique=True,
        index=True,
        min_length=1,
        max_length=40,
        pattern=r'^([0-9a-zA-Z]+-?[0-9a-zA-Z]*)*[^-]$',
        python_type=str,
        not_none=True,
        required=True,
        watermark='Enter your organization name',
        example='netalic',
        label='Name',
    )

