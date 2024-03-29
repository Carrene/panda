import io
import os
from os.path import dirname, abspath, join

from bddrest.authoring import when, status, response, given
from nanohttp import settings

from panda.models import Member, Application

from .helpers import LocalApplicationTestCase


TEST_DIR = abspath(dirname(__file__))
STUFF_DIR = join(TEST_DIR, 'stuff')
VALID_ICON_PATH = join(STUFF_DIR, 'icon-150x150.jpg')
INVALID_FORMAT_ICON_PATH = join(STUFF_DIR, 'test.pdf')
INVALID_MAXIMUM_SIZE_ICON_PATH = join(STUFF_DIR, 'icon-550x550.jpg')
INVALID_MINIMUM_SIZE_ICON_PATH = join(STUFF_DIR, 'icon-50x50.jpg')
INVALID_RATIO_ICON_PATH = join(STUFF_DIR, 'icon-150x100.jpg')
INVALID_MAXMIMUM_LENGTH_ICON_PATH = join(
    STUFF_DIR,
    'icon-maximum-length.jpg'
)


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member1 = Member(
            email='member1@example.com',
            title='member1',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123abcABC',
            role='member'
        )
        cls.application1 = Application(
            title='application1',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=member1
        )
        session.add(cls.application1)

        member2 = Member(
            email='member2@example.com',
            title='member2',
            first_name='member2_first_name',
            last_name='member2_last_name',
            password='123abcABC',
            role='member'
        )
        cls.application2 = Application(
            title='application2',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner=member2
        )
        session.add(cls.application2)
        session.commit()

    def test_update_application(self):
        self.login(email='member1@example.com', password='123abcABC')
        title = 'oauth application'
        redirectUri = 'http://example.com/oauth2'

        with self.given(
            f'Updating the application',
            f'/apiv1/applications/id:{self.application1.id}',
            f'UPDATE',
            multipart=dict(title=title, redirectUri=redirectUri)
        ):
            assert status == 200
            assert response.json['id'] == self.application1.id
            assert response.json['title'] == title
            assert response.json['redirectUri'] == redirectUri

            when(
                'Trying to pass with the balnk redirect URI and without title',
                multipart=given - 'title' | dict(redirectUri='')
            )
            assert status == '706 Redirect URI Is Blank'

            when(
                'Redirect URI contains only spaces and without title',
                multipart=given - 'title' | dict(redirectUri=' ')
            )
            assert status == '706 Redirect URI Is Blank'

            when(
                'Trying to pass with the blank title and without redirect URI',
                multipart=given - 'redirectUri' | dict(title='')
            )
            assert status == '712 Title Is Blank'

            when(
                'Title contains only spaces and without redirect URI',
                multipart=given - 'redirectUri' | dict(title=' ')
            )
            assert status == '712 Title Is Blank'

            when(
                'Trying to pass with wrong application id',
                url_parameters=dict(id=self.application2.id)
            )
            assert status == 404

            when(
                'The application not exist with this id',
                url_parameters=dict(id=0)
            )
            assert status == 404

            when(
                'Trying to pass using id is alphabetical',
                url_parameters=dict(id='a')
            )
            assert status == 404

            when('Trying to pass with empty form', multipart={})
            assert status == 400

            with open(VALID_ICON_PATH, 'rb') as f:
                when(
                    'Updating the icon of application',
                    multipart=dict(icon=io.BytesIO(f.read()))
                )
                assert response.json['icon'].startswith(
                    settings.storage.base_url
                )

            with open(INVALID_MAXIMUM_SIZE_ICON_PATH, 'rb') as f:
                when(
                    'The icon size is exceeded the maximum size',
                    multipart=dict(icon=io.BytesIO(f.read()))
                )
                assert status == '618 Maximum allowed width is:  200, '\
                    'but the  550 is given.'

            with open(INVALID_MINIMUM_SIZE_ICON_PATH, 'rb') as f:
                when(
                    'The icon size is less than minimum size',
                    multipart=dict(icon=io.BytesIO(f.read()))
                )
                assert status == '618 Minimum allowed width is:  100, '\
                    'but the  50 is given.'

            with open(INVALID_RATIO_ICON_PATH, 'rb') as f:
                when(
                    'Aspect ratio of the icon is invalid',
                    multipart=dict(icon=io.BytesIO(f.read()))
                )
                assert status == '619 Invalid aspect ratio '\
                    'Only 1/1 is accepted.'

            with open(INVALID_FORMAT_ICON_PATH, 'rb') as f:
                when(
                    'Format of the icon is invalid',
                    multipart=dict(icon=io.BytesIO(f.read()))
                )
                assert status == '620 Invalid content type, Valid options ' \
                    'are: image/jpeg, image/png'

            with open(INVALID_MAXMIMUM_LENGTH_ICON_PATH, 'rb') as f:
                when(
                    'The maxmimum length of icon is invalid',
                    multipart=dict(icon=io.BytesIO(f.read()))
                )
                assert status == '621 Cannot store files larger than: '\
                    '51200 bytes'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

