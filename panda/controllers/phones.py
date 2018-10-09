from nanohttp import context, json, RestController, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession

from ..models import Member
from ..tokens import PhoneNumberActivationToken
from ..validators import phone_number_validator


class PhoneNumberActivationTokenController(RestController):

    @authorize
    @phone_number_validator
    @json
    @commit
    def create(self):
        phone = context.form['phoneNumber']
        current_member = Member.current()
        if current_member.phone is not None:
            raise HTTPStatus('615 Member Has The Phone Number')

        member = DBSession.query(Member) \
            .filter(Member.phone == phone) \
            .one_or_none()
        if member is not None:
            raise HTTPStatus('616 Phone Number Already Exists')

        DBSession.add(Member.create_otp(phone, context.identity.id))
        token = PhoneNumberActivationToken(dict(phoneNumber=phone))
        return dict(activationToken=token.dump())

