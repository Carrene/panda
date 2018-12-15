from cas import CASPrincipal
from nanohttp import context, HTTPStatus, HTTPForbidden
from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession
from sqlalchemy_media import store_manager

from .models import Member, ApplicationMember
from .oauth.tokens import AccessToken


class Authenticator(StatefulAuthenticator):

    @staticmethod
    def safe_member_lookup(condition):
        member = DBSession.query(Member).filter(condition).one_or_none()

        if member is None:
            raise HTTPStatus('603 Incorrect Email Or Password')

        return member

    @store_manager(DBSession)
    def create_principal(self, member_id=None, session_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        principal =  member.create_jwt_principal()

        if context.identity:
            payload = context.identity.payload
            payload.update(principal.payload)
            principal.payload = payload

        return principal

    def create_refresh_principal(self, member_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        return member.create_refresh_principal()

    def validate_credentials(self, credentials):
        email, password = credentials
        member = self.safe_member_lookup(Member.email == email)

        if not member.validate_password(password):
            return None

        return member

    def verify_token(self, encoded_token):
        if not encoded_token.startswith('oauth2-accesstoken'):
            return CASPrincipal.load(encoded_token)

        access_token = AccessToken.load(encoded_token.split(' ')[1])
        if not DBSession.query(ApplicationMember) \
                .filter(
                    ApplicationMember.application_id ==  \
                    access_token.application_id,
                    ApplicationMember.member_id == access_token.member_id
                ) \
                .one_or_none():
            raise HTTPForbidden()

        return access_token

