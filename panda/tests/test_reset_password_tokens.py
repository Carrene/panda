from bddrest.authoring import response, Update, Remove, when, status
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import ResetPasswordEmail
from panda.tests.helpers import LoadApplicationTestCase


class TestResetPasswordTokenApplication(LoadApplicationTestCase):
    __configuration__ = '''
      messaging:
        default_messenger: restfulpy.mockup.MockupMessenger
    '''

    def test_ask_reset_password_tokens(self):
        messanger = create_messenger()
        email = 'already.added@example.com'

        with self.given(
            'Ask a reset password token',
            '/apiv1/resetpasswordtokens',
            'ASK',
            form=dict(email=email)
        ):
            assert status == 200
            assert response.json['email'] == email

            task = ResetPasswordEmail.pop()
            task.do_(None)

            assert messanger.last_message['to'] == email

            assert settings.reset_password.callback_url == \
                messanger.last_message['body']['reset_password_callback_url']

            assert messanger.last_message['subject'] ==\
                'Reset your CAS account password'

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
                form=Update(email='user@example.com')
            )
            assert status == 200
            assert response.json['email'] == 'user@example.com'

            when(
                'Request without email parametes',
                form=Remove('email')
            )
            assert status == '701 Invalid email format'

