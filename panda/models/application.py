import base64

from restfulpy.orm import DeclarativeBase, Field, relationship
from sqlalchemy import Unicode, Integer, Binary, ForeignKey


class Application(DeclarativeBase):
    __tablename__ = 'application'

    id = Field(Integer, primary_key=True)

    member_id = Field(Integer, ForeignKey('member.id'))

    title = Field(Unicode(100))
    redirect_uri = Field(Unicode(100))
    secret = Field(Binary(32))

    member = relationship(
        'Member',
        back_populates='applications',
        protected=True
    )

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title,
            redirectUri=self.redirect_uri,
            secret=base64.encodebytes(self.secret),
            memberId=self.member_id
        )

    def validate_secret(self, secret):
        try:
            return self.secret == base64.decodebytes(bytes(secret, 'utf-8'))
        except:
            return False