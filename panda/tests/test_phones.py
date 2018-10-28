import time

from bddrest.authoring import response, Update, when, status, Remove
from nanohttp import settings

from panda.models import Member
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import PhoneNumberActivationToken


class TestPhone(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        cls.session = cls.create_session(expire_on_commit=True)
        cls.member1 = Member(
            email='user1@example.com',
            title='user1',
            password='123456',
            role='member'
        )
        cls.session.add(cls.member1)

        cls.member2 = Member(
            email='user2@example.com',
            title='user2',
            password='123456',
            role='member',
            phone='+989121234567'
        )
        cls.session.add(cls.member2)
        cls.session.commit()

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

            self.logout()
            self.login('user2@example.com', password='123456')
            when(
                'The member has a phone number',
                form=dict(phoneNumber='+989351234567'),
                authorization=self._authentication_token
            )
            assert status == '615 Member Has The Phone Number'

    def test_bind_phone_number(self):
        self.login('user1@example.com', password='123456')

        phone_number = '+989351234567'
        code, token = self._create_activation_code_and_token(
                phone_number,
                self.member1.id
            )

        with self.given(
            'Binding the phone number to member',
            '/apiv1/phonenumbers',
            'BIND',
            form=dict(activationCode=code, activationToken=token)
        ):
            assert status == 200
            assert response.json['phoneNumber'] == phone_number

            self.session.expire(self.member1)
            assert self.member1.phone == phone_number

            code, token = self._create_activation_code_and_token(
                '+989351234567',
                self.member1.id
            )
            when(
                'The phone number has existed',
                form=Update(activationCode=code, activationToken=token)
            )
            assert status == '616 Phone Number Already Exists'

            code, token = self._create_activation_code_and_token(
                '+98361234567',
                self.member1.id
            )
            when(
                'The member has the phone number',
                form=Update(activationCode=code, activationToken=token)
            )
            assert status == '615 Member Has The Phone Number'

            when('Activation code invalid', form=Update(activationCode='code'))
            assert status == '617 Activation Code Is Not Valid'

            when('Activation code invalid', form=Update(activationCode='code'))
            assert status == '617 Activation Code Is Not Valid'

            when('Removing the activation code', form=Remove('activationCode'))
            assert status == '714 Activation Code Not In Form'

            when('Removing the token', form=Remove('activationToken'))
            assert status == '715 Activation Token Not In Form'

            code, token = self._create_activation_code_and_token(
                '+98371234567',
                self.member2.id
            )
            when(
                'The member has the phone number',
                form=Update(activationCode=code, activationToken=token)
            )
            assert status == 403

            when('Token is malformd', form=Update(activationToken='token'))
            assert status == '611 Malformed Token'

            settings.phone.activation_token.max_age = 0.3
            activation_token = PhoneNumberActivationToken(dict(
                PhoneNumber='+989351234567',
                memberId=self.member1.id
            )).dump()
            time.sleep(1)
            when(
                'Token is expired',
                form=Update(activationToken=activation_token)
            )
            assert status == '609 Token Expired'

            when('Trying to pass with unauthorized member', authorization=None)
            assert status == 401

    def _create_activation_code_and_token(self, phone_number, id):
        code = Member.generate_activation_code(phone_number, str(id))
        token = PhoneNumberActivationToken(dict(
            phoneNumber=phone_number,
            memberId=id
        ))
        return(code, token.dump())

