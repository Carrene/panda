import time

from bddrest.authoring import response, Update, when, status, Remove
from nanohttp import settings

from panda.models import Member
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import RegistrationToken


class TestRegisteration(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            name='user1',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_register_member(self):
        email = 'user@example.com'
        title = 'nickname'
        name = 'nickname'
        password = '123abdABD'
        registration_token = RegistrationToken(dict(email=email)).dump()

        with self.given(
            'Register a member',
            '/apiv1/members',
            'REGISTER',
            json=dict(
                title=title,
                name=name,
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
                'Invalid name max length',
                json=Update(name='a' * (20 + 1))
            )
            assert status == '733 At Most 20 Characters Are Valid For Name'

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

            when('Trying to pass without name', json=Remove('name'))
            assert status == '731 Name Not In Form'

            when('Trying to pass with none name', json=Update(name=None))
            assert status == '732 Name Is Null'

            when('The name have numbers', json=Update(name='name1'))
            assert status == '716 Invalid Name Format'

            when('Trying to pass without password', json=Remove('password'))
            assert status == '728 Password Not In Form'

