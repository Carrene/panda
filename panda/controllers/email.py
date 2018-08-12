from nanohttp import json, context, settings, HTTPStatus
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from panda.tokens import RegisterationToken
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

        token = RegisterationToken(dict(email=email))
        DBSession.add(
            RegisterEmail(
                to=email,
                subject='Register your CAS account',
                body={
                    'registerationToken': token.dump(),
                    'registerationCallbackUrl':
                    settings.registeration.callback_url
                }
            )
        )
        return dict(email=email)

