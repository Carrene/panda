from bddrest.authoring import response, Update, when, status
from restfulpy.messaging import create_messenger

from panda.controllers.root import Root
from panda.models import RegisterEmail, Member
from panda.tests.helpers import LocadApplicationTestCase


class TestRegisteration(LocadApplicationTestCase):
    __controller_factory__ = Root
    __configuration__ = '''
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
            assert status == 200
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
                'Invalid title format',
                form=Update(password='123AAAaaa', title='1username')
            )
            assert status == '705 Invalid title format'

            when ('Duplicate title', form=Update(title='username'))
            assert status == '604 Title is already registered'

            when ('Duplicate Email', form=Update(title='user_name'))
            assert status == '601 Email address is already registered'

            when (
                'The toekn has been damaged',
                form=Update(title='user_name', ownership_token='token')
            )
            assert status == '704 Invalid token'

