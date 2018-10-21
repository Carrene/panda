from os.path import dirname, abspath, join

from bddrest.authoring import status, response, Update, Remove, when

from panda.models import Member
from panda.tests.helpers import LocalApplicationTestCase


TEST_DIR = abspath(dirname(__file__))
AVATARS_DIR = join(TEST_DIR, 'stuff/avatars')
VALID_AVATAR_PATH = join(AVATARS_DIR, '225*225.jpg')
INVALID_FORMAT_AVATAR_PATH = join(AVATARS_DIR, 'test.pdf')
INVALID_MAXIMUM_SIZE_AVATAR_PATH = join(AVATARS_DIR, '1100*1100.jpg')
INVALID_MINIMUM_SIZE_AVATAR_PATH = join(AVATARS_DIR, '50*50.jpg')
INVALID_RATIO_AVATAR_PATH = join(AVATARS_DIR, '300*200.jpg')


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

    def test_update_name(self):
        self.login(email=self.member.email, password='123456')

        with self.given(
            'Updating name of member',
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
            assert response.json['id'] == self.member.id
            assert response.json['name'] == 'username'
            assert response.json['avatar'] is None

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
                'Invalide the maxmimum size of avatar',
                multipart=dict(avatar=INVALID_MAXIMUM_SIZE_AVATAR_PATH)
            )
            assert status == 720

            when(
                'Invalide the minimum size of avatar',
                multipart=dict(avatar=INVALID_MAXIMUM_SIZE_AVATAR_PATH)
            )
            assert status == 720

            when(
                'Invalide aspect ratio of avatar',
                multipart=dict(avatar=INVALID_RATIO_AVATAR_PATH)
            )
            assert status == 721

            when(
                'Invalide format of avatar',
                multipart=dict(avatar=INVALID_FORMAT_AVATAR_PATH)
            )
            assert status == 721

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

