from nanohttp import json, context, HTTPNotFound
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from ..exceptions import HTTPEmailAddressAlreadyRegistered, \
    HTTPTitleAlreadyRegistered
from ..models import Member
from ..validators import email_validator, title_validator


class AvailabilityController(RestController):

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
            raise HTTPEmailAddressAlreadyRegistered()
        return {}

    @title_validator
    def title_validation(self, title):
        if DBSession.query(Member.title).filter(Member.title == title).count():
            raise HTTPTitleAlreadyRegistered()
        return {}

