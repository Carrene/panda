from bddrest.authoring import when, status, response, given

from panda.models import Member, Organization
from panda.tests.helpers import LocalApplicationTestCase


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC',
            role='member'
        )
        member1 = Member(
            email='already1.added@example.com',
            title='username1',
            password='123abcABC',
            role='member'
        )


        organization = Organization(
            title='organization-title',
            members=[member, member1],
        )
        session.add(organization)
        session.commit()

    def test_list_organization(self):
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            'List of organization',
            '/apiv1/organizationmembers',
            'LIST',
        ):
            assert status == 200

