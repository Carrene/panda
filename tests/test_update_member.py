import io
from os.path import dirname, abspath, join

from bddrest.authoring import status, response, Update, Remove, when
from nanohttp import settings

from panda.models import Member

from .helpers import LocalApplicationTestCase


TEST_DIR = abspath(dirname(__file__))
STUFF_DIR = join(TEST_DIR, 'stuff')
VALID_AVATAR_PATH = join(STUFF_DIR, 'avatar-225x225.jpg')
INVALID_FORMAT_AVATAR_PATH = join(STUFF_DIR, 'test.pdf')
INVALID_MAXIMUM_SIZE_AVATAR_PATH = join(STUFF_DIR, 'avatar-550x550.jpg')
INVALID_MINIMUM_SIZE_AVATAR_PATH = join(STUFF_DIR, 'avatar-50x50.jpg')
INVALID_RATIO_AVATAR_PATH = join(STUFF_DIR, 'avatar-300x200.jpg')
INVALID_MAXMIMUM_LENGTH_AVATAR_PATH = join(
    STUFF_DIR,
    'avatar-maximum-length.jpg'
)


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member1 = Member(
            email='user1@example.com',
            title='member1_title',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123456',
            role='member'
        )
        session.add(cls.member1)

        cls.member2 = Member(
            email='user2@example.com',
            title='member2_title',
            first_name='member2_first_name',
            last_name='member2_last_name',
            password='123456',
            role='member'
        )
        session.add(cls.member2)
        session.commit()

    def test_update_member(self):
        self.login(email=self.member1.email, password='123456')

        with self.given(
            f'Updating profile of member',
            f'/apiv1/members/id: {self.member1.id}',
            f'UPDATE',
            multipart=dict(firstName='username')
        ):
            assert status == 200
            assert response.json['id'] == self.member1.id
            assert response.json['firstName'] == 'username'
            assert response.json['avatar'] is None

            when(
                'Trying to pass using id is alphabetical',
                url_parameters=dict(id='not-integer')
            )
            assert status == 404

            when(
                'Trying to pass with wrong member id',
                url_parameters=dict(id=self.member2.id)
            )
            assert status == 404

            when(
                'The member not exist with this id',
                url_parameters=dict(id=10)
            )
            assert status == 404

            when(
                'Trying to pass without first name parameter',
                multipart=Remove('firstName')
            )
            assert status == 400

            when('The name have numbers', multipart=Update(firstName='name1'))
            assert status == '716 Invalid Name Format'

            when(
                'The first name is less than the minimum length',
                multipart=Update(firstName='n')
            )
            assert status == '716 Invalid Name Format'

            when(
                'The first name have numbers',
                multipart=Update(firstName='name1')
            )
            assert status == '716 Invalid Name Format'

            when(
                'Invalid name max length',
                multipart=Update(firstName='a' * (40 + 1))
            )
            assert status == '733 At Most 20 Characters Are Valid For ' \
                'First Name'

            when(
                'Trying to pass with redundant parameters in form',
                multipart=Update(title='title')
            )
            assert status == '717 Invalid field, only the firstName, ' \
                'lastName and avatar parameters are accepted'

            with open(VALID_AVATAR_PATH, 'rb') as f:
                when(
                    'Updating the avatar of member',
                    multipart=dict(avatar=io.BytesIO(f.read()))
                )
                assert response.json['avatar'].startswith(
                    settings.storage.base_url
                )

            with open(INVALID_MAXIMUM_SIZE_AVATAR_PATH, 'rb') as f:
                when(
                    'The avatar size is exceeded the maximum size',
                    multipart=dict(avatar=io.BytesIO(f.read()))
                )
                assert status == '618 Maximum allowed width is:  300, '\
                    'but the  550 is given.'

            with open(INVALID_MINIMUM_SIZE_AVATAR_PATH, 'rb') as f:
                when(
                    'The avatar size is less than minimum size',
                    multipart=dict(avatar=io.BytesIO(f.read()))
                )
                assert status == '618 Minimum allowed width is:  200, '\
                    'but the  50 is given.'

            with open(INVALID_RATIO_AVATAR_PATH, 'rb') as f:
                when(
                    'Aspect ratio of the avatar is invalid',
                    multipart=dict(avatar=io.BytesIO(f.read()))
                )
                assert status == '619 Invalid aspect ratio '\
                    'Only 1/1 is accepted.'

            with open(INVALID_FORMAT_AVATAR_PATH, 'rb') as f:
                when(
                    'Format of the avatar is invalid',
                    multipart=dict(avatar=io.BytesIO(f.read()))
                )
                assert status == '620 Invalid content type, Valid options '\
                    'are: image/jpeg, image/png'

            with open(INVALID_MAXMIMUM_LENGTH_AVATAR_PATH, 'rb') as f:
                when(
                    'The maxmimum length of avatar is invalid',
                    multipart=dict(avatar=io.BytesIO(f.read()))
                )
                assert status == '621 Cannot store files larger than: '\
                    '51200 bytes'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

