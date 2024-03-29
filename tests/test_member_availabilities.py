from bddrest.authoring import response, status, Update, when, Remove

from panda.models import Member

from .helpers import LocalApplicationTestCase


class TestAvailabilities(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123abcABC',
            role='member'
        )
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
            assert status == '701 Invalid Email Format'

            when('Email not contain dot', form=Update(email='user@examplecom'))
            assert status == '701 Invalid Email Format'

            when('Invalid email format', form=Update(email='@example.com'))
            assert status == '701 Invalid Email Format'

            when('Email not contains any domain', form=Update(email='us@.com'))
            assert status == '701 Invalid Email Format'

            when(
                'Email address is already registered',
                form=Update(email='already.added@example.com')
            )
            assert status == '601 Email Address Is Already Registered'

            when('Request without email parametes', form=Remove('email'))
            assert status == '722 Email Not In Form'

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
            assert status == '705 Invalid Title Format'

            when('Title is already registered', form=Update(title='username'))
            assert status == '604 Title Is Already Registered'

            when('Request without title parametes', form=Remove('title'))
            assert status == '718 Title Not In Form'

