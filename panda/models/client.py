import base64

from restfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Unicode, Integer, Binary, ForeignKey


class Client(DeclarativeBase):
    __tablename__ = 'client'

    id = Field(Integer, primary_key=True)
    
    member_id = Field(Integer, ForeignKey('member.id'))
    
    title = Field(Unicode(100))
    redirect_uri = Field(Unicode(100))
    secret = Field(Binary(32))

    member = relationship('Member', back_populates='clients', protected=True)

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            redirect_uri=self.redirect_uri,
            secret=base64.encodebytes(self.secret),
            member_id=self.member_id
        )

