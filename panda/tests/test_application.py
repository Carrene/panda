import base64
import hashlib
import os

from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase, RandomMonkeyPatch


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)
        session.flush()

        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner_id=member.id
        )
        session.add(cls.application)
        session.commit()

    def test_define_application(self):
        title = 'example_application'
        redirect_uri = 'http://example.com/oauth2'

        self.login(
            email='already.added@example.com',
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )

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

    def test_metadata(self):
        with self.given(
            'Test metadata verb',
            '/apiv1/applications',
            'METADATA'
        ):
            assert status == 200

    def test_get_application(self):
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            f'Get a application using application id',
            f'/apiv1/applications/id:{self.application.id}',
            f'GET',
        ):
            assert status == 200
            assert response.json['id'] == self.application.id

            when('Trying to pass with wrong id', url_parameters=dict(id=50))
            assert status == '605 We Don\'t Recognize This Application'

            when(
                'Trying to pass with invalid the type id',
                url_parameters=dict(id='id')
            )
            assert status == 400

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

    def test_list_application(self):
        with self.given(
            'Get all available applications',
            '/apiv1/applications',
            'LIST'
        ):
            assert status == 200
            assert len(response.json) == 3
            assert response.json[0]['secret'] == None
            assert response.json[0]['redirectUri'] == None
            assert response.json[0]['ownerId'] == None
            assert response.json[0]['title'] != None

            when('The request with form parameter', form=dict(param='param'))
            assert status == '707 Form Not Allowed'

            when('Trying to sorting response', query=dict(sort='id'))
            assert status == 200
            assert response.json[0]['id'] == 1
            assert response.json[1]['id'] == 2
            assert response.json[2]['id'] == 3

            when('Sorting the response descending', query=dict(sort='-id'))
            assert response.json[0]['id'] == 3
            assert response.json[1]['id'] == 2
            assert response.json[2]['id'] == 1

            when('Trying pagination response', query=dict(take=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

            when('Trying pagination with skip', query=dict(take=1, skip=1))
            assert response.json[0]['id'] == 2
            assert len(response.json) == 1

            when('Trying filtering response', query=dict(id=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

