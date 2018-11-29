from bddrest.authoring import when, status, response, given

from panda.models import Member, Organization, OrganizationMember
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
        session.add(member)

        member1 = Member(
            email='already1.added@example.com',
            title='username1',
            password='123abcABC',
            role='member'
        )
        session.add(member1)

        organization = Organization(
            title='organization-title',
            members=[member, member1],
        )
        session.add(organization)

        organization1 = Organization(
            title='organization-title1',
            members=[member],
        )
        session.add(organization1)
        session.flush()

        organization_member1 = OrganizationMember(
            member_id = member1.id,
            organization_id = organization1.id,
            role = 'member',
        )
        session.add(organization_member1)

        organization2 = Organization(
            title='organization-title2',
            members=[member, member1],
        )
        session.add(organization2)

        organization3 = Organization(
            title='organization-title3',
            members=[member, member1],
        )
        session.add(organization3)
        organization4 = Organization(
            title='organization-title4',
            members=[member],
        )
        session.add(organization4)
        session.commit()

    def test_list_organization(self):
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            'List of organization',
            '/apiv1/organizationmembers',
            'LIST',
        ):
            import pudb; pudb.set_trace()  # XXX BREAKPOINT
            assert status == 200
            a = response.json

