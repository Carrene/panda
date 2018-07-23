from bddrest.authoring import response, Update, when
from restfulpy.messaging import create_messenger
from restfulpy.orm import DBSession
from restfulpy.testing import ApplicableTestCase

from panda.controllers.root import Root
from panda.models import Member, RegisterEmail


class TestEmailApplication(ApplicableTestCase):
    __controller_factory__ = Root

    __configuration__ = '''
    activation:
      secret: activation-secret
      url: http://cas.carrene.com/register

    messaging:
      default_messenger: restfulpy.mockup.MockupMessenger
    '''

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title = 'user',
        )
        member.is_active = True
        DBSession.add(member)
        DBSession.commit()

    def test_version(self):
        messanger = create_messenger()

        call = dict(
            title='Request whitout email parameters',
            url='/apiv1/emails',
            verb='CLAIM',
            form=dict()
        )

        with self.given(**call):
            assert response.status == 701

            when('Email not contain @', form=Update(email='userexample.com'))
            assert response.status == 701

            when('Email not contain dot', form=Update(email='user@examplecom'))
            assert response.status == 701

            when('Invalid format email', form=Update(email='@example.com'))
            assert response.status == 701

            when('Email not contain domain', form=Update(email='user@.com'))
            assert response.status == 701

            when(
                'Email address is already registered',
                form=Update(email='already.added@example.com')
            )
            assert response.status == 601

            when(
                'Claim an email',
                form=Update(email='user@example.com')
            )
            assert response.status == 200

            task = RegisterEmail.pop()
            task.do_(None)

            assert 'email' in response.json

            assert 'register_token' in messanger.last_message['body']
            assert 'register_url' in messanger.last_message['body']

