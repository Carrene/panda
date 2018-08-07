import os
import base64
from urllib.parse import urlparse, parse_qs

import itsdangerous
from bddrest.authoring import Update, Remove, when, status, response
from nanohttp import settings

from panda.models import Member, Client
from panda.tests.helpers import LocadApplicationTestCase


class TestAccessToken(LocadApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cls.member = Member(
            email='member@example.com',
            title='member_Title',
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

    def test_create_authorization_code(self):
        self.login(
            email=self.member.email,
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )
        scope='profile'
        state='123456'
        redirect_uri='http://example2.com/oauth2'

        with self.given(
            'Create authorization code',
            '/apiv1/authorizationcodes',
            'CREATE',
            query=dict(
                client_id=self.client.id,
                scope=scope,
                state=state,
                redirect_uri=redirect_uri
            )
        ):
            authorization_code = response.json['authorizationCode']

        with self.given(
            'Create access token',
            '/apiv1/accesstokens',
            'CREATE',
            form=dict(
                client_id=self.client.id,
                secret=base64.encodebytes(self.client.secret),
                code=authorization_code,
            )
        ):
            assert status == 200






