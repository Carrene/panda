import itsdangerous
from nanohttp import settings
from restfulpy.principal import BaseJWTPrincipal

from .exceptions import HTTPTokenExpired, HTTPMalformedToken


class RegistrationToken(BaseJWTPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)

        except itsdangerous.SignatureExpired:
            raise HTTPTokenExpired()

        except itsdangerous.BadSignature:
            raise HTTPMalformedToken()

    @classmethod
    def get_config(cls):
        return settings.registration

    @property
    def email(self):
        return self.payload.get('email')


class ResetPasswordToken(BaseJWTPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)

        except itsdangerous.SignatureExpired:
            raise HTTPTokenExpired()

        except itsdangerous.BadSignature:
            raise HTTPMalformedToken()

    @classmethod
    def get_config(cls):
        return settings.reset_password

    @property
    def email(self):
        return self.payload.get('email')


class PhoneNumberActivationToken(BaseJWTPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)

        except itsdangerous.SignatureExpired:
            raise HTTPTokenExpired()

        except itsdangerous.BadSignature:
            raise HTTPMalformedToken()

    @classmethod
    def get_config(cls):
        return settings.phone.activation_token

    @property
    def phone_number(self):
        return self.payload.get('phoneNumber')

    @property
    def member_id(self):
        return self.payload.get('memberId')


class OrganizationInvitationToken(BaseJWTPrincipal):

    @classmethod
    def load(cls, token):
        try:
            return super().load(token)

        except itsdangerous.SignatureExpired:
            raise HTTPTokenExpired()

        except itsdangerous.BadSignature:
            raise HTTPMalformedToken()

    @classmethod
    def get_config(cls):
        return settings.organization_invitation

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

