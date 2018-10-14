import base64
import os

from bddrest.authoring import Remove, Update, when, status, response

from panda.models import Member, Application
from panda.oauth import AccessToken, AuthorizationCode
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
        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=cls.member
        )
        session.add(cls.application)
        session.commit()

    def test_create_access_token(self):
        self.login(email=self.member.email, password='123abcABC')

        authorization_code_principal = AuthorizationCode(dict(
            scopes=['title'],
            state='123456',
            rediectUri='http://example2.com/oauth2',
            applicationId=self.application.id,
            memberId=self.member.id
        ))
        authorization_code = authorization_code_principal.dump()

        with self.given(
            'Create a access token',
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
            access_token_principal = AccessToken.load(access_token)
            assert access_token_principal.application_id == self.application.id
            assert access_token_principal.scopes == ['title']
            assert access_token_principal.member_id == self.member.id

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

