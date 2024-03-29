from bddrest.authoring import response, status, when, Update

from panda.models import Member

from .helpers import LocalApplicationTestCase


class TestLogin(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

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
            assert status == '603 Incorrect Email Or Password'

            when('Not exist email', form=Update(email='user@example.com'))
            assert status == '603 Incorrect Email Or Password'

            when('Invalid email format', form=Update(email='user.com'))
            assert status == '701 Invalid Email Format'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

