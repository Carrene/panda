import itsdangerous
from nanohttp import json, context, settings
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from panda.models import Member, ResetPasswordEmail
from panda.validators import email_validator


class ResetPasswordTokenController(ModelRestController):

    @commit
    @json
    @email_validator
    def ask(self):
        email = context.form.get('email')

        if not DBSession.query(Member.email).filter(Member.email == email)\
                .count():
            return dict(email=email)

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.reset_password.secret)

        token = serializer.dumps(email)

        DBSession.add(
            ResetPasswordEmail(
                to=email,
                subject='Reset your CAS account password',
                body={
                    'reset_password_token': token,
                    'reset_password_callback_url':
                    settings.reset_password.callback_url
                }
            )
        )

        return dict(email=email)

