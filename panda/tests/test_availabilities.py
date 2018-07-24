from bddrest.authoring import response, status, Update, when, Remove
from restfulpy.testing import ApplicableTestCase

from panda.controllers.root import Root
from panda.models import Member, RegisterEmail


class TestAvailabilitiesApplication(ApplicableTestCase):
    __controller_factory__ = Root

    @classmethod
    def mockup(cls):
        member = Member(email='already.added@example.com', title='user')
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_email_availabilities(self):
        email = 'user@example.com'

        with self.given(
            'The availability of an email address',
            '/apiv1/availabilities/emails',
            'CHECK',
            form=dict(email=email)
        ):
            assert response.status == 200

            when('Email not contain @', form=Update(email='userexample.com'))
            assert status == '701 Invalid email format'

            when('Email not contain dot', form=Update(email='user@examplecom'))
            assert status == '701 Invalid email format'

            when('Invalid email format', form=Update(email='@example.com'))
            assert status == '701 Invalid email format'

            when('Email not contains any domain', form=Update(email='us@.com'))
            assert status == '701 Invalid email format'

            when(
                'Email address is already registered',
                form=Update(email='already.added@example.com')
            )
            assert status == '601 Email address is already registered'

            when('Request without email parametes', form=Remove('email'))
            assert status == '701 Invalid email format'

