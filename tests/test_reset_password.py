from bddrest.authoring import response, Update, Remove, when, status, given
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import ResetPasswordEmail, Member
from panda.tokens import ResetPasswordToken

from .helpers import LocalApplicationTestCase


class TestResetPassword(LocalApplicationTestCase):
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
                form=Update(email='user@example.com')
            )
            assert status == 200
            assert response.json['email'] == 'user@example.com'

            when(
                'Request without email parametes',
                form=given - 'email' + dict(a='a')
            )
            assert status == '722 Email Not In Form'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

    def test_reset_password(self):
        session = self.create_session()
        messanger = create_messenger()
        email = 'already.added@example.com'
        password = 'NewPassword123'

        hash_old_password = session.query(Member).one().password
        reset_password_principal = ResetPasswordToken(dict(email=email))

        with self.given(
            'Reset your CAS account password',
            '/apiv1/passwords',
            'RESET',
            form=dict(
                password=password,
                resetPasswordToken=reset_password_principal.dump()
            )
        ):
            assert status == 200

            hash_new_password = session.query(Member).one().password
            assert hash_new_password != hash_old_password

            when(
                'Trying to pass a short password',
                form=Update(password='1Aa')
            )
            assert status == '702 Invalid Password Length'

            when(
                'Trying to a pass long password',
                form=Update(password='1Aa123456789abcdeABCDE')
            )
            assert status == '702 Invalid Password Length'

            when('Request without password parameter', form=Remove('password'))
            assert status == '728 Password Not In Form'

            when(
                'Trying to pass without reset password token in request',
                form=Remove('resetPasswordToken')
            )
            assert status == '730 Reset Password Token Not In Form'

            when(
                'The token has been damaged',
                form=Update(resetPasswordToken='token')
            )
            assert status == '611 Malformed Token'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

