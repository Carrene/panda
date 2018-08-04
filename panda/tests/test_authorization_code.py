import os
from urllib.parse import urlparse, parse_qs

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Client
from panda.tests.helpers import LocadApplicationTestCase


class TestAuthorizationCode(LocadApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cls.member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session.add(cls.member)
        session.flush()

        cls.client = Client(
            title='oauth',
            redirect_uri='http://example.com/oauth2',
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

        with self.given(
            'Create authorization code',
            '/apiv1/authorizationcodes',
            'CREATE',
            query=dict(
                client_id=self.client.id,
                scope='profile',
                state='123456',
                redirect_uri='http://example.com/oauth2'
            )
        ):
            assert status == 302

            url_parse = urlparse(response.headers['location'])
            url_query_string = {
                k: v[0] for k, v in parse_qs(url_parse.query).items()
            }

            assert url_query_string['state'] == '123456'
            assert url_query_string['scope'] == 'profile'

            # Related to the state test case
            when(
                'Trying pass to without clint_id parameter',
                query=Remove('state')
            )
            assert status == 302
            assert 'state'not in url_query_string['state']

            # Related to the client id test case
            when(
                'Tring to pass not exist client',
                query=Update(client_id='1000')
            )
            assert status == '605 We don\'t recognize this client'

            when(
                'Trying pass to without clint_id parameter',
                query=Remove('client_id')
            )
            assert status == '605 We don\'t recognize this client'

            # Related to the scope test case
            when(
                'Trying to pass invalid scope name',
                query=Update(scope='profiles')
            )
            assert status == '606 Invalid scope'

            when(
                'Trying pass to without scope parameter',
                query=Remove('scope')
            )
            assert status == '606 Invalid scope'

            # related to the form parameters
            when('Trying to pass with form parameters', form=dict(a='a'))
            assert status == '707 Form not allowed'

            when(
                'An authorization member trying to create authorization code',
                authorization=None
            )
            assert status == 401

