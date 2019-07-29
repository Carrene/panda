from bddrest.authoring import response, Update, when, status, given
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import RegisterEmail, Member
from panda.tokens import RegistrationToken

from .helpers import LocalApplicationTestCase


class TestEmail(LocalApplicationTestCase):
    __configuration__ = '''
      messaging:
        default_messenger: restfulpy.mockup.MockupMessenger
    '''

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            first_name='member_first_name',
            last_name='member_last_name',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_claim_email_ownership(self):
        messenger = create_messenger()
        email = 'user@example.com'

        with self.given(
            'Claim a email',
            '/apiv1/emails',
            'CLAIM',
            query=dict(a=1),
            form=dict(email=email)
        ):
            assert response.status == 200
            assert 'email' in response.json
            assert response.json['email'] == email

            task = RegisterEmail.pop()
            task.do_(None)

            assert messenger.last_message['to'] == email
            token = messenger.last_message['body']['registration_token']
            registration_token = RegistrationToken.load(token)
            assert registration_token.payload['email'] == email
            assert registration_token.payload['a'] == '1'
            assert settings.registration.callback_url == \
                messenger.last_message['body']['registration_callback_url']
            assert messenger.last_message['subject'] == \
                'Register your CAS account'

            when('Email not contain @', form=Update(email='userexample.com'))
            assert status == '701 Invalid Email Format'

            when('Email not contain dot', form=Update(email='user@examplecom'))
            assert status == '701 Invalid Email Format'

            when('Invalid email format', form=Update(email='@example.com'))
            assert status == '701 Invalid Email Format'

            when(
                'Email not contains any domain',
                form=Update(email='user@.com')
            )
            assert status == '701 Invalid Email Format'

            when(
                'Email address is already registered',
                form=Update(email='already.added@example.com')
            )
            assert status == '601 Email Address Is Already Registered'

            when(
                'Request without email parametes',
                form=given - 'email' + dict(a='a')
            )
            assert status == '722 Email Not In Form'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

