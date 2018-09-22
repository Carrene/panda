import os
from urllib.parse import urlparse, parse_qs

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Application
from panda.oauth import AuthorizationCode
from panda.tests.helpers import LocalApplicationTestCase


class TestAuthorizationCode(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cls.member = Member(
            email='member@example.com',
            title='member_Title',
            password='123abcABC',
            role='member'
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

    def test_create_authorization_code(self):
        self.login(
            email=self.member.email,
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )
        scopes = 'title'
        state = '123456'
        redirect_uri = 'http://example2.com/oauth2'

        with self.given(
            'Create authorization code',
            '/apiv1/authorizationcodes',
            'CREATE',
            query=dict(
                applicationId=self.application.id,
                scopes=scopes,
                state=state,
                redirectUri=redirect_uri
            )
        ):
            assert status == 200

            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            assert authorization_code['scopes'] == scopes.split(',')
            assert authorization_code['applicationTitle'] == \
                self.application.title
            assert authorization_code['applicationId'] == self.application.id
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
                query=Remove('redirectUri')
            )
            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            location_parse = urlparse(authorization_code['location'])
            location_query_string = {
                k: v[0] for k, v in parse_qs(location_parse.query).items()
            }
            location_redirect_uri = location_parse.geturl().split('?')[0]
            assert location_redirect_uri == self.application.redirect_uri

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

            # Related to the application id tests
            when(
                'Trying to pass not existing application',
                query=Update(applicationId='1000')
            )
            assert status == '605 We Don\'t Recognize This Application'
            when(
                'Trying to pass without clint_id parameter',
                query=Remove('applicationId')
            )
            assert status == '605 We Don\'t Recognize This Application'

            # Related to the scope tests
            when(
                'Trying to pass multi scope',
                query=Update(scopes='title,email')
            )
            assert status == 200
            authorization_code = \
                AuthorizationCode.load(response.json['authorizationCode'])
            assert authorization_code['scopes'] == 'title,email'.split(',')

            when(
                'Trying to pass invalid scope name',
                query=Update(scopes='profiles')
            )
            assert status == '606 Invalid Scope'

            when(
                'Trying to pass without scope parameter',
                query=Remove('scopes')
            )
            assert status == '606 Invalid Scope'

            # Related to the form parameters
            when('Trying to pass with form parameters', form=dict(a='a'))
            assert status == '707 Form Not Allowed'

            # Related to the unauthorization member
            when(
                'An unauthorized member trying to create authorization code',
                authorization=None
            )
            assert status == 401

