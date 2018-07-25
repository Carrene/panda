from restfulpy.orm import DeclarativeBase, Field
from sqlalchemy import Unicode, Integer


class Member(DeclarativeBase):
    __tablename__ = 'member'

    id = Field(Integer, primary_key=True)

    email = Field(Unicode(100), unique=True, index=True)

    title = Field(Unicode(100))

