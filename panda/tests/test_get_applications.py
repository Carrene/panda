import base64
import hashlib
import os

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase, RandomMonkeyPatch


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
        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(cls.application)
        session.commit()

    def test_get_application(self):
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            f'Get a application using application id',
            f'/apiv1/applications/id:{self.application.id}',
            f'GET',
        ):
            assert status == 200
            assert response.json['id'] == self.application.id
            assert response.json['secret'] is not None

            when('Trying to pass with wrong id', url_parameters=dict(id=0))
            assert status == 404

            when('Type of id is invalid', url_parameters=dict(id='id'))
            assert status == 404

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

