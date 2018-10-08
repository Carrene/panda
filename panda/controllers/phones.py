from nanohttp import context, json, RestController, HTTPStatus
from restfulpy.orm import commit, DBSession

from ..models import Member
from ..validators import phone_number_validator


class PhoneNumberActivationTokenController(RestController):

    @phone_number_validator
    @json
    @commit
    def create(self):
        phone = context.form['phoneNumber']
        member = DBSession.query(Member) \
            .filter(Member.phone == phone) \
            .one_or_none()
        if member is None:
            raise HTTPStatus('616 Phone Already Exists')

        token = PhoneNumberActivationTokenController(dict(phoneNumber=phone))
        return dict(activationToken=token.dump())
