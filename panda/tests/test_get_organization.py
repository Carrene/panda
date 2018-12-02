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

        member1 = Member(
            email='member1@example.com',
            title='member1',
            password='123456',
            role='member'
        )
        session.add(member1)

        cls.organization1 = Organization(
            title='organization-title-1',
        )
        session.add(cls.organization1)
        session.flush()

        organization_member1 = OrganizationMember(
            member_id=owner1.id,
            organization_id=cls.organization1.id,
            role='owner',
        )
        session.add(organization_member1)
        session.commit()

    def test_get_organization(self):
        self.login(email='owner1@example.com', password='123456')

        with self.given(
            f'Get one of my organization using id',
            f'/apiv1/organizations/id: {self.organization1.id}',
            f'GET',
        ):
            assert status == 200
            assert response.json['id'] == self.organization1.id

            when('Trying to pass with wrong id', url_parameters=dict(id=0))
            assert status == 404

            when('Type of id is invalid', url_parameters=dict(id='id'))
            assert status == 404

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

            self.logout()
            self.login(email='member1@example.com', password='123456')
            when(
                'The user not member of organization',
                authorization=self._authentication_token
            )
            assert status == 404

