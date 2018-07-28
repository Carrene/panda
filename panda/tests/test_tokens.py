from bddrest.authoring import response, status, when, Update

from panda.tests.helpers import LoadApplicationTestCase


class TestTokenApplication(LoadApplicationTestCase):

    def test_create_token(self):
        email = 'already.added@example.com'
        password = '123abcABC'

        with self.given(
            'Create a login token',
            '/apiv1/tokens',
            'CREATE',
            form=dict(email=email, password=password)
        ):
            assert status == 200
            assert 'token' in response.json

            when('Invalid password', form=Update(password='123aA'))
            assert status == '603 Incorrect email or password'

            when('Not exist email', form=Update(email='user@example.com'))
            assert status == '603 Incorrect email or password'

            when('Invalid email format', form=Update(email='user.com'))
            assert status == '701 Invalid email format'

