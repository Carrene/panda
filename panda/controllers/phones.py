from nanohttp import context, json, RestController, validate, HTTPForbidden
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession

from ..exceptions import HTTPPhoneNumberAlreadyExists, \
    HTTPActivationCodeNotValid, HTTPSecondPhoneNumber
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
            raise HTTPSecondPhoneNumber()

        member = DBSession.query(Member) \
            .filter(Member.phone == phone) \
            .one_or_none()
        if member is not None:
            raise HTTPPhoneNumberAlreadyExists()

        DBSession.add(Member.create_otp(phone, context.identity.reference_id))
        token = PhoneNumberActivationToken(dict(
            phoneNumber=phone,
            memberId=context.identity.reference_id
        ))
        return dict(activationToken=token.dump())


class PhoneNumberController(RestController):

    @authorize
    @validate(
        activationCode=dict(required='714 Activation Code Not In Form'),
        activationToken=dict(required='715 Activation Token Not In Form')
    )
    @json
    @commit
    def bind(self):
        activation_token = context.form.get('activationToken')
        token = PhoneNumberActivationToken.load(activation_token)

        result = Member.verify_activation_code(
            token.phone_number,
            token.member_id,
            context.form.get('activationCode')
        )
        if result is False:
            raise HTTPActivationCodeNotValid()

        if context.identity.reference_id != token.member_id:
            raise HTTPForbidden()

        member = DBSession.query(Member) \
            .filter(Member.phone == token.phone_number) \
            .one_or_none()
        if member is not None:
            raise HTTPPhoneNumberAlreadyExists()

        current_member = Member.current()
        if current_member.phone is not None:
            raise HTTPSecondPhoneNumber()

        current_member.phone = token.phone_number
        DBSession.add(current_member)
        return dict(phoneNumber=token.phone_number)

