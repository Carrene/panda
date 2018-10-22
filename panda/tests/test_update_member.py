from os.path import dirname, abspath, join

from bddrest.authoring import status, response, Update, Remove, when

from panda.models import Member
from panda.tests.helpers import LocalApplicationTestCase


TEST_DIR = abspath(dirname(__file__))
AVATARS_DIR = join(TEST_DIR, 'stuff/avatars')
VALID_AVATAR_PATH = join(AVATARS_DIR, '225*225.jpg')
INVALID_FORMAT_AVATAR_PATH = join(AVATARS_DIR, 'test.pdf')
INVALID_MAXIMUM_SIZE_AVATAR_PATH = join(AVATARS_DIR, '550*550.jpg')
INVALID_MINIMUM_SIZE_AVATAR_PATH = join(AVATARS_DIR, '50*50.jpg')
INVALID_RATIO_AVATAR_PATH = join(AVATARS_DIR, '300*200.jpg')
INVALID_MAXMIMUM_LENGTH_AVATAR_PATH = join(AVATARS_DIR, 'maximum-length.jpg')
INVALID_AVATAR_PATH = join(AVATARS_DIR, 'not-exist.jpg')


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member = Member(
            email='user1@example.com',
            title='member_title',
            password='123456',
            role='member'
        )
        session.add(cls.member)
        session.commit()

    def test_update_member(self):
        self.login(email=self.member.email, password='123456')

        with self.given(
            'Updating profile of member',
            '/apiv1/members',
            'UPDATE',
            multipart=dict(name='username')
        ):
            assert status == 200
            assert response.json['id'] == self.member.id
            assert response.json['name'] == 'username'
            assert response.json['avatar'] is None

            when(
                'Trying to pass without name parameter',
                multipart=Remove('name')
            )
            assert status == 400

            when('The name have numbers', form=Update(name='name1'))
            assert status == '716 Invalid Name Format'

            when(
                'The name is less than the minimum length',
                form=Update(name='n')
            )
            assert status == '716 Invalid Name Format'

            when(
                'Invalid the max lenght of name',
                multipart=Update(name='name name name name n')
            )
            assert status == '716 Invalid Name Format'

            when(
                'Trying to pass with redundant parameters in form',
                multipart=Update(title='title')
            )
            assert status == '717 Invalid Field, Only The Name Parameter ' \
                'Is Accepted'

            when(
                'Updating the avatar of member',
                multipart=dict(avatar=VALID_AVATAR_PATH)
            )
            assert response.json['avatar'] is not None

            when(
                'Invalid the maxmimum size of avatar',
                multipart=dict(avatar=INVALID_MAXIMUM_SIZE_AVATAR_PATH)
            )
            assert status == 618

            when(
                'Invalid the minimum size of avatar',
                multipart=dict(avatar=INVALID_MAXIMUM_SIZE_AVATAR_PATH)
            )
            assert status == 618

            when(
                'Invalid the aspect ratio of avatar',
                multipart=dict(avatar=INVALID_RATIO_AVATAR_PATH)
            )
            assert status == 619

            when(
                'Invalid the format of avatar',
                multipart=dict(avatar=INVALID_FORMAT_AVATAR_PATH)
            )
            assert status == 620

            when(
                'Invalid the maxmimum length of avatar',
                multipart=dict(avatar=INVALID_MAXMIMUM_LENGTH_AVATAR_PATH)
            )
            assert status == 621

            when(
                'Invalid the avatar path',
                multipart=dict(avatar=INVALID_AVATAR_PATH)
            )
            assert status == 622

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

