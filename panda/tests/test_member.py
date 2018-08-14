import os
import time

from bddrest.authoring import status, response, when, Update
from nanohttp import settings

from panda.models import Member, Client
from panda.oauth.tokens import AccessToken
from panda.tests.helpers import LocadApplicationTestCase


class TestMemberProfile(LocadApplicationTestCase):

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

        cls.client = Client(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            member_id=cls.member.id
        )
        session.add(cls.client)
        session.commit()

    def test_member_profile(self):
        access_token_payload = dict(
            client_id=self.client.id,
            member_id=self.member.id,
            scope='title',
        )
        access_token = AccessToken(access_token_payload).dump().decode()

        with self.given(
            'Get member profile',
            f'/apiv1/members/id: {self.member.id}',
            'GET',
            headers={'authorization': f'oauth2-accesstoken {access_token}'},
        ):
            assert status == 200
            assert response.json['title'] == self.member.title

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
            assert status == '610 Malformed access token'

            access_token_payload['scope'] = 'title+email'
            access_token = AccessToken(access_token_payload).dump().decode()
            when(
                'Trying to pass with multi scope',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert response.json['title'] == self.member.title
            assert response.json['email'] == self.member.email

            settings.access_token.max_age = 0.1
            access_token = AccessToken(access_token_payload).dump().decode()
            time.sleep(1)
            when(
                'Trying to pass with expired token',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert status == '609 Token expired'

