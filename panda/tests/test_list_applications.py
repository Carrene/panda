import os

from bddrest.authoring import when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC',
            role='member'
        )

        application1 = Application(
            title='oauth1',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(application1)

        application2 = Application(
            title='oauth2',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(application2)

        application3 = Application(
            title='oauth3',
            redirect_uri='http://example3.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(application3)

        session.commit()

    def test_list_application(self):
        with self.given(
            'Get all available applications',
            '/apiv1/applications',
            'LIST'
        ):
            assert status == 200
            assert len(response.json) == 3
            assert response.json[0]['secret'] == None
            assert response.json[0]['redirectUri'] == None
            assert response.json[0]['ownerId'] == None
            assert response.json[0]['title'] != None

            when('The request with form parameter', form=dict(param='param'))
            assert status == '707 Form Not Allowed'

            when('Trying to sorting response', query=dict(sort='id'))
            assert status == 200
            assert response.json[0]['id'] == 1
            assert response.json[1]['id'] == 2
            assert response.json[2]['id'] == 3

            when('Sorting the response descending', query=dict(sort='-id'))
            assert response.json[0]['id'] == 3
            assert response.json[1]['id'] == 2
            assert response.json[2]['id'] == 1

            when('Trying pagination response', query=dict(take=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

            when('Trying pagination with skip', query=dict(take=1, skip=1))
            assert response.json[0]['id'] == 2
            assert len(response.json) == 1

            when('Trying filtering response', query=dict(id=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

