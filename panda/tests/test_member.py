import os
import time

from bddrest.authoring import status, response, when
from nanohttp import settings

from panda.models import Member, Application
from panda.oauth.tokens import AccessToken
from panda.tests.helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cls.member = Member(
            email='member@example.com',
            title='member_title',
            password='123abcABC'
        )
        session.add(cls.member)
        session.flush()

        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner_id=cls.member.id
        )
        session.add(cls.application)
        session.commit()

    def test_get_member(self):
        access_token_payload = dict(
            applicationId=self.application.id,
            memberId=self.member.id,
            scopes=['title']
        )
        access_token = AccessToken(access_token_payload).dump().decode()

        with self.given(
            'Get member according to scopes',
            f'/apiv1/members/id: {self.member.id}',
            'GET',
            headers={'authorization': f'oauth2-accesstoken {access_token}'},
        ):
            assert status == 200
            assert response.json['title'] == self.member.title
            assert response.json['id'] == self.member.id

            when(
                'Trying to pass using another member id',
                url_parameters=dict(id='2')
            )
            assert status == '403 Forbidden'

            when(
                'Trying to pass using id is alphabetical',
                url_parameters=dict(id='a')
            )
            assert status == '403 Forbidden'

            when('Trying to pass without headers', headers={})
            assert status == '403 Forbidden'

            when(
                'Trying to pass with damege token',
                headers={'authorization': 'oauth2-accesstoken token'}
            )
            assert status == '610 Malformed Access Token'

            access_token_payload['scopes'] = ['title', 'email']
            access_token = AccessToken(access_token_payload).dump().decode()
            when(
                'Trying to pass with multi scope',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert response.json['title'] == self.member.title
            assert response.json['email'] == self.member.email
            assert response.json['id'] == self.member.id

            settings.access_token.max_age = 0.1
            access_token = AccessToken(access_token_payload).dump().decode()
            time.sleep(1)
            when(
                'Trying to pass with expired token',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert status == '609 Token Expired'

    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/members', 'METADATA'):
            assert status == 200

