import os
from urllib.parse import urlparse, parse_qs

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Client
from panda.oauth import AuthorizationCode
from panda.tests.helpers import LocadApplicationTestCase


class TestAuthorizationCode(LocadApplicationTestCase):

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
        scope='title'
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
            assert status == 200

            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            assert authorization_code['scope'] == scope
            assert authorization_code['clientTitle'] == self.client.title
            assert authorization_code['clientId'] == self.client.id
            assert authorization_code['memberId'] == self.member.id
            assert authorization_code['email'] == self.member.email

            location_parse = urlparse(authorization_code['location'])
            location_query_string = {
                k: v[0] for k, v in parse_qs(location_parse.query).items()
            }
            location_redirect_uri = location_parse.geturl().split('?')[0]
            assert location_redirect_uri == redirect_uri
            assert location_query_string['state'] == state

            # Related to the redirect uri tests
            when(
                'Trying to pass without redirect uri parameter',
                query=Remove('redirect_uri')
            )
            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            location_parse = urlparse(authorization_code['location'])
            location_query_string = {
                k: v[0] for k, v in parse_qs(location_parse.query).items()
            }
            location_redirect_uri = location_parse.geturl().split('?')[0]
            assert location_redirect_uri == self.client.redirect_uri

            # Related to the state tests
            when(
                'Trying to pass without state parameter',
                query=Remove('state')
            )
            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            location_parse = urlparse(authorization_code['location'])
            location_query_string = {
                k: v[0] for k, v in parse_qs(location_parse.query).items()
            }
            assert 'state' not in location_query_string

            # Related to the client id tests
            when(
                'Trying to pass not existing client',
                query=Update(client_id='1000')
            )
            assert status == '605 We don\'t recognize this client'

            when(
                'Trying to pass without clint_id parameter',
                query=Remove('client_id')
            )
            assert status == '605 We don\'t recognize this client'

            # Related to the scope tests
            when(
                'Trying to pass multi scope',
                query=Update(scope='title+email')
            )
            assert status == 200
            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            assert authorization_code['scope'] == 'title+email'

            when(
                'Trying to pass invalid scope name',
                query=Update(scope='profiles')
            )
            assert status == '606 Invalid scope'

            when(
                'Trying to pass without scope parameter',
                query=Remove('scope')
            )
            assert status == '606 Invalid scope'

            # Related to the form parameters
            when('Trying to pass with form parameters', form=dict(a='a'))
            assert status == '707 Form not allowed'

            # Related to the unauthorization member
            when(
                'An unauthorized member trying to create authorization code',
                authorization=None
            )
            assert status == 401

