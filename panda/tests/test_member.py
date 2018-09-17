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
        admin = Member(
            email='admin@example.com',
            title='admin_title',
            password='123abcABC',
            role='admin'
        )
        session.add(admin)

        owner = Member(
            email='owner@example.com',
            title='owner_title',
            password='123abcABC',
            role='member'
        )
        session.add(owner)
        session.flush()

        cls.member = Member(
            email='member@example.com',
            title='member_title',
            password='123abcABC',
            role='member'
        )
        session.add(cls.member)
        session.flush()

        cls.application1 = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner_id=owner.id
        )
        cls.application1.members.append(cls.member)
        session.add(cls.application1)

        cls.application2 = Application(
            title='oauth',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner_id=owner.id
        )
        session.add(cls.application2)
        session.commit()

    def test_get_member_by_me(self):
        access_token_payload = dict(
            applicationId=self.application1.id,
            memberId=self.member.id,
            scopes=['title']
        )
        access_token = AccessToken(access_token_payload).dump().decode()

        with self.given(
            'Get member according to scopes',
            f'/apiv1/members/id: me',
            'GET',
            headers={'authorization': f'oauth2-accesstoken {access_token}'},
        ):
            assert status == 200
            assert response.json['title'] == self.member.title
            assert response.json['id'] == self.member.id

            when('Trying to pass without headers', headers={})
            assert status == 401

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

            access_token_payload = dict(
                applicationId=self.application2.id,
                memberId=self.member.id,
                scopes=['title']
            )
            access_token = AccessToken(access_token_payload).dump().decode()
            when(
                'The member revoke the authorization application',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert status == 403

        self.login(email=self.member.email, password='123abcABC')
        with self.given(
            'Get member as member',
            '/apiv1/members/id:me',
            'GET',
        ):
            assert status == 200
            assert response.json['id'] == self.member.id

            when('Trying to get another member', url_parameters=dict(id=1))
            assert status == 403


    def test_metadata(self):
        with self.given('Test metadata verb', '/apiv1/members', 'METADATA'):
            assert status == 200

    def test_get_member_by_id(self):
        self.login(email='admin@example.com',password='123abcABC')
        with self.given(
            'Get member as admin',
            '/apiv1/members/id:1',
            'GET',
        ):
            assert status == 200
            assert response.json['id'] == 1

            when('Get another member as admin', url_parameters=dict(id=2))
            assert response.json['id'] == 2

            when('Trying to pass with unauthorized member', authorization=None)
            assert status == 401

