import base64

from nanohttp import context
from restfulpy.orm import DeclarativeBase, OrderingMixin, PaginationMixin, \
    FilteringMixin, Field, relationship
from sqlalchemy import Unicode, Integer, Binary, ForeignKey


class Application(DeclarativeBase, OrderingMixin, PaginationMixin,
                  FilteringMixin):
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
            redirectUri=self.safe_redirect_uri,
            memberId=self.safe_member_id,
            secret=self.safe_secret
        )

    def validate_secret(self, secret):
        try:
            return self.secret == base64.decodebytes(bytes(secret, 'utf-8'))
        except:
            return False

    def am_i_owner(self):
        return context.identity and self.member_id == context.identity.id

    @property
    def safe_secret(self):
        return base64.encodebytes(self.secret) if self.am_i_owner() else None

    @property
    def safe_redirect_uri(self):
        return self.redirect_uri if self.am_i_owner() else None

    @property
    def safe_member_id(self):
        return self.member_id if self.am_i_owner() else None

