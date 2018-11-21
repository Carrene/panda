import time

from bddrest.authoring import when, status, response, Update, given
from nanohttp import settings

from panda.models import Member, Organization
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import OrganizationInvitationToken


class TestApplication(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session(expire_on_commit=True)
        cls.member1 = Member(
            email='user1@example.com',
            title='user1',
            password='123456',
            role='member'
        )
        cls.member2 = Member(
            email='user2@example.com',
            title='user2',
            password='123456',
            role='member'
        )
        session.add(cls.member2)

        cls.organization = Organization(
            title='organization-title',
            members=[cls.member1],
        )
        session.add(cls.organization)
        session.commit()

    def test_join_organization(self):
        self.login(email=self.member2.email, password='123456')
        payload = dict(
            email=self.member2.email,
            organizationId=self.organization.id,
            memberId=self.member2.id,
            ownerId=self.member1.id,
            role='member',
        )
        token = OrganizationInvitationToken(payload)

        with self.given(
            'Joining to the organization has successfully',
            '/apiv1/organizations',
            'JOIN',
            form=dict(token=token.dump())
        ):
            assert status == 200
            assert response.json['title'] == self.organization.title

            when('Trying again for join to the organization')
            assert status == '623 Already In This Organization'

            payload['organizationId'] = 100
            token = OrganizationInvitationToken(payload)
            when(
                'The organization not exist',
                form=Update(token=token.dump())
            )
            assert status == 404

            when(
                'Trying to pass without invitation token in form',
                form=given - 'token' | dict(a='a')
            )
            assert status == '727 Token Not In Form'

            when(
                'Trying to pass with malformed token',
                form=Update(token='Malformed token')
            )
            assert status == '611 Malformed Token'

            settings.organization_invitation.max_age = 0.3
            token = OrganizationInvitationToken(payload)
            invitation_token = token.dump()
            time.sleep(1)
            when(
                'Trying to pass with expired token',
                form=Update(token=invitation_token)
            )
            assert status == '609 Token Expired'

            when('Trying to pass without form parameters', form={})
            assert status == 400

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

