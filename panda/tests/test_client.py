import base64
import hashlib

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member
from panda.tests.helpers import LocadApplicationTestCase, RandomPatch


class TestClient(LocadApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_define_client(self):
        title = 'example_client'
        redirect_uri = 'http://example.com/oauth2'

        self.login(
            email='already.added@example.com',
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with RandomPatch(
            b'2X\x95z\x14\x7f\x80\xe2\xd1\xdeD\xf6\xd3\x9ea\x90uZ \
            \x00\xb3mG@\xd0\x1a"\xc7-V\r8\x11'
        ), self.given(
            'The client has successfully defined',
            '/apiv1/clients',
            'DEFINE',
            form=dict(title=title, redirect_uri=redirect_uri)
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['redirect_uri'] == redirect_uri

            secret = base64.encodebytes(hashlib.pbkdf2_hmac(
                'sha256',
                str(response.json['member_id']).encode(),
                RandomPatch.random(32),
                100000,
                dklen=32
            )).decode()
            assert response.json['secret'] == secret

            when('Trying to pass duplicate title')
            assert status == 200

            when('Trying to pass with balnk title', form=Update(title=' '))
            assert status == '705 Invalid title format'

            when(
                'Trying to pass without title parameter',
                form=Remove('title')
            )
            assert status == '705 Invalid title format'

            when(
                'Trying to pass with balnk title',
                form=Update(redirect_uri=' ')
            )
            assert status == '706 Redirect uri is blank'

            when(
                'Trying to pass without title parameter',
                form=Remove('redirect_uri')
            )
            assert status == '706 Redirect uri is blank'

        self.logout()

        with self.given(
            'An unauthorized member trying to define client',
            '/apiv1/clients',
            'DEFINE',
            form=dict(title=title, redirect_uri=redirect_uri)
        ):
            assert status == 401

