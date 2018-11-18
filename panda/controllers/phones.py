from nanohttp import context, json, RestController, HTTPStatus, validate, \
    HTTPForbidden
from restfulpy.authorization import authorize
from restfulpy.orm import commit, DBSession

from ..exceptions import HTTPPhoneNumberAlreadyExists, \
    HTTPActivationCodeNotValid
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
        activation_token_principal =PhoneNumberActivationToken. \
            load(context.form.get('activationToken'))

        result = Member.verify_activation_code(
            activation_token_principal.phone_number,
            activation_token_principal.member_id,
            context.form.get('activationCode')
        )
        if result is False:
            raise HTTPActivationCodeNotValid()

        if context.identity.reference_id != activation_token_principal.member_id:
            raise HTTPForbidden()

        member = DBSession.query(Member) \
            .filter(Member.phone == activation_token_principal.phone_number) \
            .one_or_none()
        if member is not None:
            raise HTTPPhoneNumberAlreadyExists()

        current_member = Member.current()
        if current_member.phone is not None:
            raise HTTPStatus('615 Member Has The Phone Number')

        current_member.phone = activation_token_principal.phone_number
        DBSession.add(current_member)
        return dict(phoneNumber=activation_token_principal.phone_number)

