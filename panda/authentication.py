from nanohttp import HTTPStatus, context, HTTPForbidden
from restfulpy.authentication import StatefulAuthenticator
from restfulpy.orm import DBSession

from .models import Member, ApplicationMember
from .oauth.tokens import AccessToken


class Authenticator(StatefulAuthenticator):

    @staticmethod
    def safe_member_lookup(condition):
        member = DBSession.query(Member).filter(condition).one_or_none()

        if member is None:
            raise HTTPStatus('603 Incorrect Email Or Password')

        return member

    def create_principal(self, member_id=None, session_id=None):
        member = self.safe_member_lookup(Member.id == member_id)
        return member.create_jwt_principal()

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
            return super().verify_token(encoded_token)

        access_token = AccessToken.load(encoded_token.split(' ')[1])
        if not DBSession.query(ApplicationMember) \
                .filter(
                    ApplicationMember.application_id == access_token.payload['applicationId'],
                    ApplicationMember.member_id == access_token.payload['memberId']
                ) \
                .one_or_none():
            raise HTTPForbidden()

        return access_token

