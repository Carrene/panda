import itsdangerous
from nanohttp import json, context, settings, HTTPStatus
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from panda.models import Member, RegisterEmail
from panda.validators import email_validator


class EmailController(ModelRestController):

    @commit
    @json
    @email_validator
    def claim(self):
        email = context.form.get('email')

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus('601 Email address is already registered')

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.registeration.secret)

        token = serializer.dumps(email)

        DBSession.add(
            RegisterEmail(
                to=email,
                subject='Register your CAS account',
                body={
                    'registeration_token': token,
                    'registeration_callback_url':
                    settings.registeration.callback_url
                }
            )
        )

        return dict(email=email)
