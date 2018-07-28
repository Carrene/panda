from bddrest.authoring import response, Update, Remove, when, status
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import RegisterEmail
from panda.tests.helpers import LoadApplicationTestCase


class TestEmailApplication(LoadApplicationTestCase):
    __configuration__ = '''
      messaging:
        default_messenger: restfulpy.mockup.MockupMessenger
    '''

    def test_claim_email_ownership(self):
        messanger = create_messenger()
        email = 'user@example.com'

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

            assert messanger.last_message['to'] == email

            assert settings.registeration.callback_url == \
                messanger.last_message['body']['registeration_callback_url']

            assert messanger.last_message['subject'] ==\
                'Register your CAS account'

            when('Email not contain @', form=Update(email='userexample.com'))
            assert status == '701 Invalid email format'

            when('Email not contain dot', form=Update(email='user@examplecom'))
            assert status == '701 Invalid email format'

            when('Invalid email format', form=Update(email='@example.com'))
            assert status == '701 Invalid email format'

            when(
                'Email not contains any domain',
                form=Update(email='user@.com')
            )
            assert status == '701 Invalid email format'

            when(
                'Email address is already registered',
                form=Update(email='already.added@example.com')
            )
            assert status == '601 Email address is already registered'

            when(
                'Request without email parametes',
                form=Remove('email')
            )
            assert status == '701 Invalid email format'

