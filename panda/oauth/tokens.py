import itsdangerous
from nanohttp import settings, HTTPStatus
from restfulpy.principal import BaseJwtPrincipal


class AuthorizationCode(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token).payload
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('607 Malformed authorization code')

    @classmethod
    def get_config(cls):
        return settings.authorization_code


class AccessToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token).payload
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('610 Malformed access token')

    @classmethod
    def get_config(cls):
        return settings.access_token

