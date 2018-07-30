from bddrest.authoring import Update, Remove, when, status

from panda.models import Member
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
        old_password_hash = session.query(Member).one().password

        self.login(
            email='already.added@example.com',
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'The password has been successfully changed',
            '/apiv1/passwords',
            'change',
            form=dict(
                current_password='123abcABC',
                new_password='NewPassword123'
            )
        ):
            assert status == 200

            new_password_hash = session.query(Member).one().password
            assert new_password_hash != old_password_hash

            when(
                'Trying to pass using the wrong password',
                form=Update(
                    current_password='123abc',
                    new_password='NewPassword123'
                )
            )
            assert status == '602 Invalid current password'

            when(
                'Trying to pass without current password parameter',
                form=Remove('current_password')
            )
            assert status == '602 Invalid current password'

            when(
                'Trying to pass a simple password',
                form=Update(new_password='123')
            )
            assert status == '703 Password not complex enough'

            when(
                'Trying to pass a short password',
                form=Update(new_password='1aA')
            )
            assert status == '702 Invalid password length'

            when(
                'Trying to pass a long password',
                form=Update(new_password='1aA123456789123456789')
            )
            assert status == '702 Invalid password length'

            when(
                'Trying to pass without new password parameter',
                form=Remove('new_password')
            )
            assert status == '702 Invalid password length'

