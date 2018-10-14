from nanohttp import json, context, HTTPStatus, settings
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit

from ..models import Member, ResetPasswordEmail
from ..tokens import ResetPasswordToken
from ..validators import password_validator, new_password_validator, \
    email_validator


class PasswordController(RestController):

    @json(prevent_empty_form=True)
    @password_validator
    @commit
    def reset(self):
        reset_password_principal = \
            ResetPasswordToken.load(context.form.get('resetPasswordToken'))

        member = DBSession.query(Member) \
            .filter(Member.email == reset_password_principal.email) \
            .one()
        member.password = context.form.get('password')
        return {}

    @json(prevent_empty_form=True)
    @authorize
    @new_password_validator
    @commit
    def change(self):
        current_password = context.form.get('currentPassword')
        new_password = context.form.get('newPassword')
        member = Member.current()

        if current_password is None or \
                not member.validate_password(current_password):
            raise HTTPStatus('602 Invalid Current Password')

        member.password = new_password
        return {}


class ResetPasswordTokenController(RestController):

    @json(prevent_empty_form=True)
    @email_validator
    @commit
    def ask(self):
        email = context.form.get('email')

        if not DBSession.query(Member.email) \
                .filter(Member.email == email) \
                .count():
            return dict(email=email)

        token = ResetPasswordToken(dict(email=email))
        DBSession.add(
            ResetPasswordEmail(
                to=email,
                subject='Reset your CAS account password',
                body={
                    'reset_password_token': token.dump(),
                    'reset_password_callback_url':
                    settings.reset_password.callback_url
                }
            )
        )
        return dict(email=email)

