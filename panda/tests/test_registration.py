from bddrest.authoring import response, Update, when, status
from restfulpy.messaging import create_messenger

from panda.models import RegisterEmail, Member
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import RegisterationToken


class TestRegisteration(LocalApplicationTestCase):
    __configuration__ = '''
    messaging:
      default_messenger: restfulpy.mockup.MockupMessenger
    '''

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_register_member(self):
        messanger = create_messenger()
        email = 'user@example.com'
        title = 'nickname'
        password = '123abdABD'
        registeration_token = RegisterationToken(dict(email=email)).dump()

        with self.given(
            'Register a member',
            '/apiv1/members',
            'REGISTER',
            form=dict(
                title=title,
                password=password,
                ownershipToken=registeration_token
            )
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['email'] == email
            assert 'id' in response.json
            assert 'X-New-JWT-Token' in response.headers

            when('Invalid password min length', form=Update(password='1Aa'))
            assert status == '702 Invalid Password Length'

            when(
                'Invalid password max length',
                form=Update(password='1Aa123456789abcdeABCDE')
            )
            assert status == '702 Invalid Password Length'

            when(
                'Invalid title format',
                form=Update(password='123AAAaaa', title='1username')
            )
            assert status == '705 Invalid Title Format'

            when ('Duplicate title', form=Update(title='username'))
            assert status == '604 Title Is Already Registered'

            when ('Duplicate Email', form=Update(title='user_name'))
            assert status == '601 Email Address Is Already Registered'

            when (
                'The toekn has been damaged',
                form=Update(title='user_name', ownershipToken='token')
            )
            assert status == '611 Malformed Token'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

