from bddrest.authoring import response, Update, Remove, when, status
from nanohttp import settings
from restfulpy.messaging import create_messenger

from panda.models import ResetPasswordEmail, Member
from panda.tests.helpers import LocadApplicationTestCase


class TestChangePassword(LocadApplicationTestCase):

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

    def test_change_password(self):
        session = self.create_session()
        hash_old_password = session.query(Member).one().password

        self.login(
            email='already.added@example.com',
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Change password',
            '/apiv1/passwords',
            'change',
            form=dict(
                current_password='123abcABC',
                new_password='Newpassword123'
            )
        ):
            assert status == 200

            hash_new_password = session.query(Member).one().password
            assert hash_new_password != hash_old_password

