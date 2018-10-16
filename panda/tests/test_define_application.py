import base64
import hashlib
import os

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase, RandomMonkeyPatch


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC',
            role='member'
        )
        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member
        )
        session.add(cls.application)
        session.commit()

    def test_define_application(self):
        title = 'example_application'
        redirect_uri = 'http://example.com/oauth2'

        self.login(email='already.added@example.com', password='123abcABC')

        with RandomMonkeyPatch(
            b'2X\x95z\x14\x7f\x80\xe2\xd1\xdeD\xf6\xd3\x9ea\x90uZ'
            b'\x00\xb3mG@\xd0\x1a"\xc7-V\r8\x11'
        ), self.given(
            'The application has successfully defined',
            '/apiv1/applications',
            'DEFINE',
            form=dict(title=title, redirectUri=redirect_uri)
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['redirectUri'] == redirect_uri

            secret = base64.encodebytes(hashlib.pbkdf2_hmac(
                'sha256',
                str(response.json['ownerId']).encode(),
                RandomMonkeyPatch.random(32),
                100000,
                dklen=32
            )).decode()
            assert response.json['secret'] == secret

            when('Trying to pass duplicate title')
            assert status == 200

            when('Trying to pass with balnk title', form=Update(title=' '))
            assert status == '705 Invalid Title Format'

            when(
                'Trying to pass without title parameter',
                form=Remove('title')
            )
            assert status == '705 Invalid Title Format'

            when(
                'Trying to pass with balnk title',
                form=Update(redirectUri=' ')
            )
            assert status == '706 Redirect URI Is Blank'

            when(
                'Trying to pass without title parameter',
                form=Remove('redirectUri')
            )
            assert status == '706 Redirect URI Is Blank'

            when('Trying to pass with empty form', form={})
            assert status == '400 Empty Form'

        self.logout()

        with self.given(
            'An unauthorized member trying to define application',
            '/apiv1/applications',
            'DEFINE',
            form=dict(title=title, redirectUri=redirect_uri)
        ):
            assert status == 401

        with self.given(
            'Test metadata verb',
            '/apiv1/applications',
            'METADATA'
        ):
            assert status == 200

            fields = response.json['fields']
            assert fields['title']['label'] is not None
            assert fields['title']['maxLength'] is not None
            assert fields['title']['minLength'] is not None
            assert fields['title']['watermark'] is not None
            assert fields['title']['name'] is not None
            assert fields['title']['not_none'] is not None
            assert fields['title']['required'] is not None

            assert fields['redirectUri']['label'] is not None
            assert fields['redirectUri']['watermark'] is not None
            assert fields['redirectUri']['name'] is not None
            assert fields['redirectUri']['not_none'] is not None
            assert fields['redirectUri']['required'] is not None
            assert fields['redirectUri']['minLength'] is not None
            assert fields['redirectUri']['maxLength'] is not None

