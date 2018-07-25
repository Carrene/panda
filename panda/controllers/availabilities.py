from nanohttp import json, context, HTTPStatus, HTTPNotFound
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from panda.models import Member
from panda.validators import email_validator, title_validator


class AvailabilitiesController(RestController):

    @json
    def check(self, subject):
        if subject == 'emails':
            return self.email_validation(context.form.get('email'))
        if subject == 'nicknames':
            return self.title_validation(context.form.get('title'))

        raise HTTPNotFound()

    @email_validator
    def email_validation(self, email):
        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus('601 Email address is already registered')

        return dict()

    @title_validator
    def title_validation(self, title):
        if DBSession.query(Member.title).filter(Member.title == title).count():
            raise HTTPStatus('604 Title is already registered')

        return dict()

