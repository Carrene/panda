import time

from bddrest.authoring import response, Update, when, status
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import Member
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import RegisterationToken
from panda.tokens import PhoneNumberActivationToken


class TestPhone(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member1 = Member(
            email='user1@example.com',
            title='user1',
            password='123456',
            role='member'
        )
        session.add(member1)

        member2 = Member(
            email='user2@example.com',
            title='user2',
            password='123456',
            role='member',
            phone='+989121234567'
        )
        session.add(member2)
        session.commit()

    def test_create_phone_number_activation_token(self):
        self.login('user1@example.com', password='123456')

        with self.given(
            'Create the phone number activation token',
            '/apiv1/phonenumberactivationtokens',
            'CREATE',
            form=dict(phoneNumber='+989351234567')
        ):
            assert status == 200
            principal_activation_token = PhoneNumberActivationToken \
                .load(response.json['activationToken'])
            assert principal_activation_token.phone_number == '+989351234567'

            when(
                'Duplicate phone number',
                form=Update(phoneNumber='+989121234567')
            )
            assert status == '616 Phone Number Already Exists'

            when(
                'The phone number is invalid',
                form=Update(phoneNumber='+9891')
            )
            assert status == '713 Invalid Phone Number'


            when('Trying to pass with unauthorized member', authorization=None)
            assert status == 401

        self.login('user2@example.com', password='123456')
        with self.given(
            'The member has a phone number',
            '/apiv1/phonenumberactivationtokens',
            'CREATE',
            form=dict(phoneNumber='+989351234567')
        ):
            assert status == '615 Member Has The Phone Number'

