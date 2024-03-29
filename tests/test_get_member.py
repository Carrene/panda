import io
import os
import time
from os.path import dirname, abspath, join

from bddrest.authoring import status, response, when
from nanohttp import settings
from sqlalchemy_media import StoreManager

from panda.models import Member, Application
from panda.oauth.tokens import AccessToken

from .helpers import LocalApplicationTestCase


TEST_DIR = abspath(dirname(__file__))
AVATAR_PATH = join(TEST_DIR, 'stuff/avatar-225x225.jpg')


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        with open(AVATAR_PATH, 'rb') as f:
            avatar = io.BytesIO(f.read())

        session = cls.create_session()
        with StoreManager(session):
            admin = Member(
                email='admin@example.com',
                title='admin_title',
                first_name='admin_first_name',
                last_name='admin_last_name',
                password='123abcABC',
                role='admin'
            )
            session.add(admin)

            owner = Member(
                email='owner@example.com',
                title='owner_title',
                first_name='owner_first_name',
                last_name='owner_last_name',
                password='123abcABC',
                role='member'
            )
            cls.member = Member(
                email='member@example.com',
                title='member_title',
                password='123abcABC',
                role='member',
                phone='+9891234567',
                first_name='member_first_name',
                last_name='member_last_name',
                avatar=avatar,
            )
            cls.application1 = Application(
                title='oauth',
                redirect_uri='http://example1.com/oauth2',
                secret=os.urandom(32),
                owner=owner,
                members=[cls.member]
            )
            session.add(cls.application1)

            cls.application2 = Application(
                title='oauth',
                redirect_uri='http://example2.com/oauth2',
                secret=os.urandom(32),
                owner=owner
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
            assert response.json['email'] is None
            assert response.json['firstName'] is None
            assert response.json['lastName'] is None
            assert response.json['avatar'] is None
            assert response.json['phone'] is None

            when('Trying to pass without authorization headers', headers={})
            assert status == 401

            when(
                'Trying to pass with damege token',
                headers={'authorization': 'oauth2-accesstoken token'}
            )
            assert status == '610 Malformed Access Token'

            access_token_payload['scopes'] = [
                'firstName',
                'lastName',
                'email',
                'avatar',
                'phone',
            ]
            access_token = AccessToken(access_token_payload).dump().decode()
            when(
                'Trying to pass with multi scope',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert response.json['firstName'] == self.member.first_name
            assert response.json['email'] == self.member.email
            assert response.json['avatar'] is not None
            assert response.json['phone'] == self.member.phone
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
                applicationId=self.application1.id,
                memberId=self.member.id,
            )
            access_token = AccessToken(access_token_payload).dump().decode()
            when(
                'Trying to pass with empty scopes in the access token',
                headers={'authorization': f'oauth2-accesstoken {access_token}'}
            )
            assert response.json['id'] == self.member.id
            assert response.json['firstName'] is None
            assert response.json['lastName'] is None
            assert response.json['email'] is None
            assert response.json['avatar'] is None
            assert response.json['phone'] is None

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

    def test_get_member_by_id(self):
        self.login(email='admin@example.com', password='123abcABC')
        with self.given(
            'Get member as admin',
            '/apiv1/members/id:1',
            'GET',
        ):
            assert status == 200
            assert response.json['id'] == 1

            when('Get another member as admin', url_parameters=dict(id=2))
            assert response.json['id'] == 2

            when(
                'Trying to get the not exist member',
                url_parameters=dict(id=200)
            )
            assert status == 404

            when(
                'Trying to pass using id is alphabetical',
                url_parameters=dict(id='a')
            )
            assert status == 404

            when('Trying to pass with unauthorized member', authorization=None)
            assert status == 401

