import base64

from nanohttp import context
from restfulpy.orm import DeclarativeBase, OrderingMixin, PaginationMixin, \
    FilteringMixin, Field, relationship
from sqlalchemy import Unicode, Integer, Binary, ForeignKey


class ApplicationMember(DeclarativeBase):
     __tablename__ = 'application_member'

     member_id = Field(Integer, ForeignKey('member.id'), primary_key=True)
     application_id = Field(
         Integer,
         ForeignKey('application.id'),
         primary_key=True
     )


class Application(DeclarativeBase, OrderingMixin, PaginationMixin,
                  FilteringMixin):
    __tablename__ = 'application'

    id = Field(Integer, primary_key=True)

    owner_id = Field(Integer, ForeignKey('member.id'))

    title = Field(
        Unicode(100),
        required=True,
        not_none=True,
        python_type=str
    )
    redirect_uri = Field(
        Unicode(100),
        required=True,
        not_none=True,
        python_type=str
    )
    secret = Field(Binary(32))

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
            secret=self.safe_secret
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

