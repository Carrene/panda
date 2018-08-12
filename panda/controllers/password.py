from nanohttp import json, context, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit

from panda.models import Member
from panda.tokens import ResetPasswordToken
from panda.validators import password_validator, new_password_validator


class PasswordController(RestController):

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
        return dict()

    @authorize
    @new_password_validator
    @json
    @commit
    def change(self):
        current_password = context.form.get('current_password')
        new_password = context.form.get('new_password')

        member = Member.current()

        if current_password is None or \
                not member.validate_password(current_password):
            raise HTTPStatus('602 Invalid current password')

        member.password = new_password

        return dict()

