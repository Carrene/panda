import itsdangerous
from nanohttp import settings, HTTPStatus
from restfulpy.principal import BaseJwtPrincipal


class RegisterationToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('611 Malformed Token')

    @classmethod
    def get_config(cls):
        return settings.registeration

    @property
    def email(self):
        return self.payload.get('email')


class ResetPasswordToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('611 Malformed Token')

    @classmethod
    def get_config(cls):
        return settings.reset_password

    @property
    def email(self):
        return self.payload.get('email')


class PhoneNumberActivationToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)
        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')
        except itsdangerous.BadSignature:
            raise HTTPStatus('611 Malformed Token')

    @classmethod
    def get_config(cls):
        return settings.phone.activation_token

    @property
    def phone_number(self):
        return self.payload.get('phoneNumber')

    @property
    def member_id(self):
        return self.payload.get('memberId')


class InviteOrganizationToken(BaseJwtPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)

        except itsdangerous.SignatureExpired:
            raise HTTPStatus('609 Token Expired')

        except itsdangerous.BadSignature:
            raise HTTPStatus('611 Malformed Token')

    @classmethod
    def get_config(cls):
        return settings.invite_organization

    @property
    def email(self):
        return self.payload.get('email')

    @property
    def organization_id(self):
        return self.payload.get('organizationId')

    @property
    def member_id(self):
        return self.payload.get('memberId')

    @property
    def owner_id(self):
        return self.payload.get('ownerId')

    @property
    def role(self):
        return self.payload.get('role')

