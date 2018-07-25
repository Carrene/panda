from bddrest.authoring import response, Update, when, status
from restfulpy.messaging import create_messenger
from restfulpy.testing import ApplicableTestCase

from panda.controllers.root import Root
from panda.models import Member, RegisterEmail


class TestMemberApplication(ApplicableTestCase):
    __controller_factory__ = Root
    __configuration__ = '''
     db:
      url: postgresql://postgres:postgres@localhost/panda_dev
      test_url: postgresql://postgres:postgres@localhost/panda_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

     registeration:
        secret: registeration-secret
        max_age: 3600  # seconds
        callback_url: http://cas.carrene.com/register

      messaging:
        default_messenger: restfulpy.mockup.MockupMessenger
    '''

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_register_member(self):
        messanger = create_messenger()
        email = 'user@example.com'
        title = 'nickname'
        password = '123abdABD'

        with self.given(
            'Claim a email',
            '/apiv1/emails',
            'CLAIM',
            form=dict(email=email)
        ):
            assert response.status == 200
            assert 'email' in response.json
            assert response.json['email'] == email

            task = RegisterEmail.pop()
            task.do_(None)

            registeration_token =\
                messanger.last_message['body']['registeration_token']

        with self.given(
            'Register a member',
            '/apiv1/members',
            'REGISTER',
            form=dict(
                email=email,
                title=title,
                password=password,
                ownership_token=registeration_token
            )
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['email'] == email
            assert 'id' in response.json
            assert 'X-New-JWT-Token' in response.headers

            when('Invalid password min length', form=Update(password='1Aa'))
            assert status == '702 Invalid password length'

            when(
                'Invalid password max length',
                form=Update(password='1Aa123456789abcdeABCDE')
            )
            assert status == '702 Invalid password length'

            when(
                'Invalid title',
                form=Update(password='123AAAaaa', title='1username')
            )
            assert status == '705 Invalid title format'

