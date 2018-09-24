import os

from bddrest.authoring import when, status, response, given

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member1 = Member(
            email='member1@example.com',
            title='member1',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member1)

        cls.application1 = Application(
            title='application1',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member1
        )
        session.add(cls.application1)

        member2 = Member(
            email='member2@example.com',
            title='member2',
            password='123abcABC',
            role='member'
        )
        session.add(member2)

        cls.application2 = Application(
            title='application2',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner=member2
        )
        session.add(cls.application2)
        session.commit()

    def test_update_application(self):
        self.login(email='member1@example.com', password='123abcABC')
        title = 'oauth application'
        redirectUri = 'http://example.com/oauth2'

        with self.given(
            f'Updating the application',
            f'/apiv1/applications/id:{self.application1.id}',
            f'UPDATE',
            form=dict(title=title, redirectUri=redirectUri)
        ):
            assert status == 200
            assert response.json['id'] == self.application1.id
            assert response.json['title'] == title
            assert response.json['redirectUri'] == redirectUri

            when(
                'Trying to pass with the balnk redirect URI and without title',
                form=given - 'title' | dict(redirectUri='')
            )
            assert status == '706 Redirect URI Is Blank'

            when(
                'Redirect URI contains only spaces and without title',
                form=given - 'title' | dict(redirectUri=' ')
            )
            assert status == '706 Redirect URI Is Blank'

            when(
                'Trying to pass with the blank title and without redirect URI',
                form=given - 'redirectUri' | dict(title='')
            )
            assert status == '712 Title Is Blank'

            when(
                'Title contains only spaces and without redirect URI',
                form=given - 'redirectUri' | dict(title=' ')
            )
            assert status == '712 Title Is Blank'

            when(
                'Trying to pass with wrong application id',
                url_parameters=dict(id=self.application2.id)
            )
            assert status == 404

            when(
                'The application not exist with this id',
                url_parameters=dict(id=10)
            )
            assert status == 404

            when(
                'Trying to pass using id is alphabetical',
                url_parameters=dict(id='a')
            )
            assert status == 404

            when('Trying to pass with empty form', form={})
            assert status == 400

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

