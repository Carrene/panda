from bddrest.authoring import when, status

from panda.models import Member

from .helpers import LocalApplicationTestCase


class TestLogout(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123abcABC',
            role='member'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_logout(self):
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            'The member has been successfully logout',
            '/apiv1/tokens',
            'INVALIDATE',
        ):
            assert status == 200

            when('Trying to pass unathorized member', authorization=None)
            assert status == 401

