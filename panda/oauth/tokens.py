import itsdangerous
from nanohttp import settings, HTTPStatus
from restfulpy.principal import BaseJwtPrincipal


class AuthorizationCode(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token).payload
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('607 Malformed Authorization Code')

    @classmethod
    def get_config(cls):
        return settings.authorization_code


class AccessToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('610 Malformed Access Token')

    @classmethod
    def get_config(cls):
        return settings.access_token

    @property
    def application_id(self):
        return self.payload.get('applicationId')

    @property
    def member_id(self):
        return self.payload.get('memberId')

    @property
    def scopes(self):
        return self.payload.get('scopes')

    @property
    def id(self):
        return self.payload.get('memberId')

    @property
    def session_id(self):
        return self.payload.get('sessionId')

    def assert_roles(self):
        pass

