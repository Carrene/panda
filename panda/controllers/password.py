import itsdangerous
from nanohttp import json, context, settings, HTTPStatus
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit
from restfulpy.authorization import authorize

from panda.models import Member
from panda.validators import password_validator, new_password_validator


class PasswordController(RestController):

    @json
    @commit
    @password_validator
    def reset(self):
        password = context.form.get('password')
        reset_password_token = context.form.get('reset_password_token')

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.reset_password.secret)

        try:
             email = serializer.loads(
                reset_password_token,
                max_age=settings.reset_password.max_age
            )

        except itsdangerous.BadSignature:
            raise HTTPStatus(status='704 Invalid token')

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

