from nanohttp import RestController, json, context
from restfulpy.authorization import authorize

from ..exceptions import HTTPIncorrectEmailOrPassword
from ..validators import email_validator


class TokenController(RestController):

    @json(prevent_empty_form=True)
    @email_validator
    def create(self):
        email = context.form.get('email')
        password = context.form.get('password')
        if email and password is None:
            raise HTTPIncorrectEmailOrPassword()

        principal = context.application.__authenticator__.\
            login((email, password))

        if principal is None:
            raise HTTPIncorrectEmailOrPassword()

        return dict(token=principal.dump())

    @authorize
    @json
    def invalidate(self):
        context.application.__authenticator__.logout()
        return {}

