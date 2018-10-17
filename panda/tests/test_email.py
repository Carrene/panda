from bddrest.authoring import response, Update, when, status, given
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import RegisterEmail, Member
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import RegisterationToken


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
            token = messenger.last_message['body']['registeration_token']
            registration_token = RegisterationToken.load(token)
            assert registration_token.payload['email'] == email
            assert registration_token.payload['a'] == '1'
            assert settings.registeration.callback_url == \
                messenger.last_message['body']['registeration_callback_url']
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
            assert status == '701 Invalid Email Format'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

