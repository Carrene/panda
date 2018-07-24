from bddrest.authoring import response, status, Update, when, Remove
from restfulpy.testing import ApplicableTestCase

from panda.controllers.root import Root
from panda.models import Member


class TestAvailabilitiesApplication(ApplicableTestCase):
    __controller_factory__ = Root

    @classmethod
    def mockup(cls):
        member = Member(email='already.added@example.com', title='nickname')
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

    def test_title_availabilities(self):
        title = 'nickname_example'

        with self.given(
            'The availability of a tile',
            '/apiv1/availabilities/nicknames',
            'CHECK',
            form=dict(title=title)
        ):
            assert response.status == 200

            when('Title contain @', form=Update(title='nick@name'))
            assert status == '705 Invalid title format'

            when('Title is already registered', form=Update(title='nickname'))
            assert status == '604 Title is already registered'

            when('Request without title parametes', form=Remove('title'))
            assert status == '705 Invalid title format'

