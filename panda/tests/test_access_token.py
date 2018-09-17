import base64
import os

from bddrest.authoring import Remove, Update, when, status, response

from panda.models import Member, Application
from panda.oauth import AccessToken
from panda.tests.helpers import LocalApplicationTestCase


class TestAccessToken(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cls.member = Member(
            email='member@example.com',
            title='member_title',
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

    def test_create_access_token(self):
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
                applicationId=self.application.id,
                scopes='title',
                state='123456',
                redirectUri='http://example2.com/oauth2'
            )
        ):
            authorization_code = response.json['authorizationCode']

        with self.given(
            'Create access token',
            '/apiv1/accesstokens',
            'CREATE',
            form=dict(
                applicationId=self.application.id,
                secret=base64.encodebytes(self.application.secret),
                code=authorization_code,
            )
        ):
            assert status == 200
            assert response.json['memberId'] == self.member.id
            access_token = response.json['accessToken']
            access_token_payload = AccessToken.load(access_token).payload
            assert access_token_payload['applicationId'] == self.application.id
            assert access_token_payload['scopes'] == ['title']
            assert access_token_payload['memberId'] == self.member.id

            when(
                'Trying to get access token using wrong application',
                form=Update(applicationId=2)
            )
            assert status == '605 We Don\'t Recognize This Application'

            when(
                'Trying to pass using damaged secret',
                form=Update(secret='damage_secret=')
            )
            assert status == '608 Malformed Secret'

            when(
                'Trying to pass using damaged secret and incorrect padding',
                form=Update(secret='secret')
            )
            assert status == '608 Malformed Secret'

            when(
                'Trying to pass without application id',
                form=Remove('applicationId')
            )
            assert status == '708 Application Id Not In Form'

            when('Trying to pass without secret', form=Remove('secret'))
            assert status == '710 Secret Not In Form'

            when('Trying to pass without code', form=Remove('code'))
            assert status == '709 Code Not In Form'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

