from bddrest.authoring import Update, Remove, when, status

from panda.models import Member
from panda.tests.helpers import LocadApplicationTestCase


class AuthorizationCodePassword(LocadApplicationTestCase):

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

    def test_get_authorization_code(self):
        with self.given(
            'Get authorization code',
            '/apiv1/authorizationcodes',
            'GET',
        ):
            assert status == 200


