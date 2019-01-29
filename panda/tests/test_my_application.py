import os

from bddrest.authoring import when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase


class TestMyApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='user@example.com',
            title='username',
            password='123abcABC',
            role='member'
        )
        application1 = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(application1)

        application2 = Application(
            title='oauth',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(application2)
        session.commit()

    def test_my_applications_list(self):
        self.login(email='user@example.com', password='123abcABC')

        with self.given(
            'Get all applications of member',
            '/apiv1/myapplications',
            'LIST'
        ):
            assert status == 200

            when(
                'Try to send form in the request',
                form=dict(parameter='parameters')
            )
            assert status == '707 Form Not Allowed'

            when('Trying to sorting response', query=dict(sort='id'))
            assert status == 200
            assert response.json[0]['id'] == 1
            assert response.json[1]['id'] == 2

            when('Sorting the response descending', query=dict(sort='-id'))
            assert response.json[0]['id'] == 2
            assert response.json[1]['id'] == 1

            when('Trying pagination response', query=dict(take=1))
            assert response.json[0]['id'] == 1

            when('Trying pagination with skip', query=dict(take=1, skip=1))
            assert response.json[0]['id'] == 2

            when('Trying filtering response', query=dict(id=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

            when('Trying to pass with unathorized member', authorization=None)
            assert status == 401

