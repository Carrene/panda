from nanohttp import json, context, HTTPStatus, HTTPNotFound
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from panda.models import Member
from panda.validators import email_validator


class AvailabilitiesController(RestController):

    @json
    def check(self, subject):
        if subject == 'emails':
            return self.email_validation(context.form.get('email'))

        raise HTTPNotFound()

    @email_validator
    def email_validation(self, email):
        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus('601 Email address is already registered')

        return dict()

