from bddrest.authoring import response, status, when, Update
from restfulpy.application import Application
from restfulpy.testing import ApplicableTestCase

from panda.authentication import Authenticator
from panda.controllers.root import Root
from panda.models import Member


class TestTokenApplication(ApplicableTestCase):
    __application__ = Application(
        'MockupApplication',
        root=Root(),
        authenticator=Authenticator()
    )
    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/panda_dev
      test_url: postgresql://postgres:postgres@localhost/panda_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    '''

    @classmethod
    def mockup(cls):
        member = Member(
            email='username@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_create_token(self):
        email = 'username@example.com'
        password = '123abcABC'

        with self.given(
            'Create a login token',
            '/apiv1/tokens',
            'CREATE',
            form=dict(email=email, password=password)
        ):
            assert status == 200
            assert 'token' in response.json

            when('Invalid password',form=Update(password='123aA'))
            assert status == '603 Incorrect email or password'

            when(
                'Invalid email',
                form=Update(password='123abcABC', email='user@example.com')
            )
            assert status == '603 Incorrect email or password'

            when('Invalid email format', form=Update(email='user.com'))
            assert status == '701 Invalid email format'

