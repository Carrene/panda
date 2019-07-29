import time

from bddrest.authoring import response, Update, when, status, Remove
from nanohttp import settings

from panda.models import Member
from panda.tokens import RegistrationToken

from .helpers import LocalApplicationTestCase


class TestRegisteration(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            first_name='user1_first_name',
            last_name='user1_last_name',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_register_member(self):
        email = 'user@example.com'
        title = 'nickname'
        first_name = 'first name'
        last_name = 'last name'
        password = '123abdABD'
        registration_token = RegistrationToken(dict(email=email)).dump()

        with self.given(
            'Register a member',
            '/apiv1/members',
            'REGISTER',
            json=dict(
                title=title,
                firstName=first_name,
                lastName=last_name,
                password=password,
                ownershipToken=registration_token.decode()
            )
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['email'] == email
            assert 'id' in response.json
            assert 'X-New-JWT-Token' in response.headers

            when('Invalid password min length', json=Update(password='1Aa'))
            assert status == '702 Invalid Password Length'

            when(
                'Invalid password max length',
                json=Update(password='1Aa123456789abcdeABCD')
            )
            assert status == '702 Invalid Password Length'

            when(
                'Invalid first name max length',
                json=Update(firstName='a' * (20 + 1))
            )
            assert status == '733 At Most 20 Characters Are Valid For First Name'

            when(
                'Invalid title format',
                json=Update(password='123AAAaaa', title='1username')
            )
            assert status == '705 Invalid Title Format'

            when('Duplicate title', json=Update(title='username'))
            assert status == '604 Title Is Already Registered'

            when('Duplicate Email', json=Update(title='user_name'))
            assert status == '601 Email Address Is Already Registered'

            when('The token has been damaged',
                json=Update(ownershipToken='token')
            )
            assert status == '611 Malformed Token'

            settings.registration.max_age = 0.3
            registration_token = RegistrationToken(dict(email=email)).dump()
            time.sleep(1)
            when(
                'The token is expired',
                json=Update(ownershipToken=registration_token.decode())
            )
            assert status == '609 Token Expired'

            when('Trying to pass with empty form', json={})
            assert status == '400 Empty Form'

            when(
                'Trying to pass without ownership token',
                json=Remove('ownershipToken')
            )
            assert status == '727 Token Not In Form'

            when('Trying to pass without title', json=Remove('title'))
            assert status == '718 Title Not In Form'

            when('Trying to pass without first name', json=Remove('firstName'))
            assert status == '731 First Name Not In Form'

            when(
                'Trying to pass with none first name',
                json=Update(firstName=None)
            )
            assert status == '732 First Name Is Null'

            when('Trying to pass without last name', json=Remove('lastName'))
            assert status == '734 Last Name Not In Form'

            when(
                'Trying to pass with none last name',
                json=Update(lastName=None)
            )
            assert status == '735 Last Name Is Null'


            when('The last name have numbers', json=Update(lastName='name1'))
            assert status == '716 Invalid Name Format'

            when(
                'Invalid last name max length',
                json=Update(lastName='a' * (20 + 1))
            )
            assert status == '736 At Most 20 Characters Are Valid For Last Name'

            when('Trying to pass without password', json=Remove('password'))
            assert status == '728 Password Not In Form'

