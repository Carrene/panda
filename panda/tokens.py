import itsdangerous
from nanohttp import settings, HTTPStatus
from restfulpy.principal import BaseJwtPrincipal, JwtPrincipal


class RegisterationToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token).payload
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('611 Malformed Token')

    @classmethod
    def get_config(cls):
        return settings.registeration


class ResetPasswordToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token).payload
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('611 Malformed Token')

    @classmethod
    def get_config(cls):
        return settings.reset_password


class AuthorizationToken(JwtPrincipal):

    @property
    def ref_id(self):
        return self.payload.get('refId')

