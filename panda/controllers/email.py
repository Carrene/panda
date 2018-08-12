from nanohttp import json, context, settings, HTTPStatus
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession, commit

from ..models import Member, RegisterEmail
from ..tokens import RegisterationToken
from ..validators import email_validator


class EmailController(RestController):

    @json(prevent_empty_form=True)
    @email_validator
    @commit
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

