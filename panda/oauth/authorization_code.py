import itsdangerous
from nanohttp import settings, HTTPStatus
from restfulpy.principal import BaseJwtPrincipal


class AuthorizationCode(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):

        try:
            return super().load(token).payload

        except itsdangerous.SignatureExpired:
            raise HTTPStatus(status='609 Token expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus(status='607 Malformed authorization code')

    @classmethod
    def get_config(cls):

        return settings.authorization_code

