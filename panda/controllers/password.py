from nanohttp import json, context, HTTPStatus, action
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit

from ..models import Member
from ..tokens import ResetPasswordToken
from ..validators import password_validator, new_password_validator


class PasswordController(RestController):

    @action(prevent_empty_form=True)
    @password_validator
    @json
    @commit
    def reset(self):
        password = context.form.get('password')
        reset_password_token = context.form.get('resetPasswordToken')
        reset_password_token_payload = \
            ResetPasswordToken.load(reset_password_token)
        email = reset_password_token_payload['email']
        member = DBSession.query(Member).filter(Member.email == email).one()
        member.password = password
        return {}

    @action(prevent_empty_form=True)
    @authorize
    @new_password_validator
    @json
    @commit
    def change(self):
        current_password = context.form.get('currentPassword')
        new_password = context.form.get('newPassword')
        member = Member.current()

        if current_password is None or \
                not member.validate_password(current_password):
            raise HTTPStatus('602 Invalid current password')

        member.password = new_password
        return {}

