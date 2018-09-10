import base64
import hashlib
import os

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase, RandomMonkeyPatch


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)

        cls.member1 = Member(
            email='member1@example.com',
            title='username1',
            password='123abcABC'
        )
        session.add(cls.member1)
        session.flush()

        cls.application1 = Application(
            title='oauth1',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner_id=cls.member1.id
        )
        session.add(cls.application1)

        cls.application2 = Application(
            title='oauth2',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner_id=cls.member1.id
        )
        session.add(cls.application2)

        cls.application1.members.append(member)
        cls.application2.members.append(member)
        session.commit()

    def test_metadata(self):
        with self.given(
            'Test metadata verb',
            '/apiv1/authorizedapplications',
            'METADATA'
        ):
            assert status == 200

    def test_list_application(self):
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            'Get all authorized applications',
            '/apiv1/authorizedapplications',
            'LIST'
        ):
            assert status == 200
            assert len(response.json) == 2
            assert response.json[0]['id'] == self.application1.id
            assert response.json[1]['id'] == self.application2.id

            when('The request with form parameter', form=dict(param='param'))
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
            assert len(response.json) == 1

            when('Trying pagination with skip', query=dict(take=1, skip=1))
            assert response.json[0]['id'] == 2
            assert len(response.json) == 1

            when('Trying filtering response', query=dict(id=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

