from bddrest.authoring import when, status, response, given

from panda.models import Member, Organization, OrganizationMember
from panda.tests.helpers import LocalApplicationTestCase


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        owner1 = Member(
            email='owner1@example.com',
            title='owner1',
            password='123456',
            role='member'
        )
        session.add(owner1)

        owner2 = Member(
            email='owner2@example.com',
            title='owner2',
            password='123456',
            role='member'
        )
        session.add(owner2)

        member1 = Member(
            email='member1@example.com',
            title='member1',
            password='123456',
            role='member'
        )
        session.add(member1)

        member2 = Member(
            email='member2@example.com',
            title='member2',
            password='123456',
            role='member'
        )
        session.add(member2)

        organization1 = Organization(
            title='organization-title-1',
            members=[owner1, owner2],
        )
        session.add(organization1)

        organization2 = Organization(
            title='organization-title-2',
            members=[owner1],
        )
        session.add(organization2)
        session.flush()

        organization_member1 = OrganizationMember(
            member_id = member1.id,
            organization_id = organization2.id,
            role = 'member',
        )
        session.add(organization_member1)

        organization3 = Organization(
            title='organization-title-3',
            members=[owner1, owner2],
        )
        session.add(organization3)
        session.flush()

        organization_member2 = OrganizationMember(
            member_id = member1.id,
            organization_id = organization3.id,
            role = 'member',
        )
        session.add(organization_member2)

        organization_member3 = OrganizationMember(
            member_id = member2.id,
            organization_id = organization3.id,
            role = 'member',
        )
        session.add(organization_member3)

        session.commit()

    def test_list_organization(self):
        self.login(email='owner1@example.com', password='123456')

        with self.given(
            'List of organization',
            '/apiv1/organizationmembers',
            'LIST',
        ):
            import pudb; pudb.set_trace()  # XXX BREAKPOINT
            assert status == 200
            a = response.json

