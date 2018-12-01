from bddrest.authoring import when, status, response

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
        )
        session.add(organization1)
        session.flush()

        organization_member1 = OrganizationMember(
            member_id = owner1.id,
            organization_id = organization1.id,
            role = 'owner',
        )
        session.add(organization_member1)

        organization_member2 = OrganizationMember(
            member_id = owner2.id,
            organization_id = organization1.id,
            role = 'owner',
        )
        session.add(organization_member2)

        organization_member3 = OrganizationMember(
            member_id = member1.id,
            organization_id = organization1.id,
            role = 'member',
        )
        session.add(organization_member3)

        organization2 = Organization(
            title='organization-title-2',
        )
        session.add(organization2)
        session.flush()

        organization_member4 = OrganizationMember(
            member_id = owner1.id,
            organization_id = organization2.id,
            role = 'owner',
        )
        session.add(organization_member4)

        session.commit()

    def test_list_organization(self):
        self.login(email='owner1@example.com', password='123456')

        with self.given(
            'List of organization',
            '/apiv1/myorganizations',
            'LIST',
        ):
            assert status == 200
            assert len(response.json) == 2

            when('The request with form parameter', form=dict(param='param'))
            assert status == '400 Form Not Allowed'

            when('Trying to sorting response', query=dict(sort='id'))
            assert response.json[0]['id'] == 1
            assert response.json[1]['id'] == 2

            when('Sorting the response descending', query=dict(sort='-id'))
            assert response.json[0]['id'] == 2
            assert response.json[1]['id'] == 1

            when('Trying pagination response', query=dict(take=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

            when('Trying pagination with skip', query=dict(take=1, skip=1))
            assert response.json[0]['id'] == 2
            assert len(response.json) == 1

            when('Trying filtering response', query=dict(id=1))
            assert response.json[0]['id'] == 1
            assert len(response.json) == 1

            self.logout()
            when(
                'Trying with an unauthorized member',
                authorization=self._authentication_token
            )
            assert status == 401

            self.login(email='member2@example.com', password='123456')
            when(
                'The user without organization',
                authorization=self._authentication_token
            )
            assert status == 200
            assert len(response.json) == 0

