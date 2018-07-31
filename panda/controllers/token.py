from nanohttp import RestController, json, context, HTTPStatus
from restfulpy.authorization import authorize

from panda.validators import email_validator


class TokenController(RestController):

    @json
    @email_validator
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')

        if email and password is None:
            raise HTTPStatus('603 Incorrect email or password')

        principal = context.application.__authenticator__.\
            login((email, password))

        if principal is None:
            raise HTTPStatus('603 Incorrect email or password')

        return dict(token=principal.dump())

    @authorize
    @json
    def invalidate(self):
        context.application.__authenticator__.logout()

        return {}
