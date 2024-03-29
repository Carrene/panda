import os

from bddrest.authoring import when, status, response

from panda.models import Member, Application

from .helpers import LocalApplicationTestCase


class TestApplicationLogout(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='already.added@example.com',
            title='username',
            first_name='member_first_name',
            last_name='member_last_name',
            password='123abcABC',
            role='member'
        )
        cls.member1 = Member(
            email='member1@example.com',
            title='username1',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123abcABC',
            role='member'
        )
        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member,
            members=[cls.member1]
        )
        session.add(cls.application)
        session.commit()

    def test_logout_application(self):
        self.login(email='member1@example.com', password='123abcABC')

        with self.given(
            f'Logout from the application using application id',
            f'/apiv1/applications/id:{self.application.id}',
            f'LOGOUT',
        ):
            assert status == 200
            assert response.json['id'] == self.application.id

            when('Trying to pass with wrong id', url_parameters=dict(id=0))
            assert status == 404

            when('The type of id is invalid', url_parameters=dict(id='id'))
            assert status == 404

            when('Send request with form parameter', form=dict(param='param'))
            assert status == '707 Form Not Allowed'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

