from bddrest.authoring import response, Update, Remove, when, status
from nanohttp import settings
from restfulpy.messaging import create_messenger
from restfulpy.testing import ApplicableTestCase

from panda.controllers.root import Root
from panda.models import Member, RegisterEmail


class TestEmailApplication(ApplicableTestCase):
    __controller_factory__ = Root
    __configuration__ = '''
      registeration:
        secret: registeration-secret
        callback_url: http://cas.carrene.com/register

      messaging:
        default_messenger: restfulpy.mockup.MockupMessenger
    '''

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='user',
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

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

            assert 'registeration_token' in messanger.last_message['body']

            assert 'registeration_callback_url' in \
                messanger.last_message['body']
            assert settings.registeration.callback_url == \
                messanger.last_message['body']['registeration_callback_url']

            assert 'to' in messanger.last_message
            assert messanger.last_message['to'] == email

            assert 'subject' in messanger.last_message
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

