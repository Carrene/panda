from bddrest.authoring import when, status, response, Update, Remove
from restfulpy.messaging import create_messenger

from panda.models import Member, Organization, OrganizationMember, \
    InviteOrganizationEmail
from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import InviteOrganizationToken


class TestApplication(LocalApplicationTestCase):
    __configuration__ = '''
      messaging:
        default_messenger: restfulpy.mockup.MockupMessenger
    '''

    @classmethod
    def mockup(cls):
        session = cls.create_session()
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

        cls.member3 = Member(
            email='user3@example.com',
            title='user3',
            password='123456',
            role='member'
        )
        session.add(cls.member3)

        cls.organization = Organization(
            title='organization-title',
            members=[cls.member1],
        )
        session.add(cls.organization)
        session.flush()

        organization_member = OrganizationMember(
            organization_id=cls.organization.id,
            member_id=cls.member2.id,
            role='member'
        )
        session.add(organization_member)
        session.commit()

    def test_invite_organization(self):
        messenger = create_messenger()
        self.login(email=self.member1.email, password='123456')

        with self.given(
            f'Inviting to the organization has successfully created',
            f'/apiv1/organizations/id: {self.organization.id}',
            f'INVITE',
            form=dict(email=self.member3.email, role='member')
        ):
            assert status == 200
            assert response.json['title'] == self.organization.title

            task = InviteOrganizationEmail.pop()
            task.do_(None)
            assert messenger.last_message['to'] == self.member3.email
            token = InviteOrganizationToken.load(
                messenger.last_message['body']['token']
            )
            assert token.role == 'member'
            assert token.email == self.member3.email
            assert token.owner_id == self.member1.id
            assert token.member_id == self.member3.id
            assert token.organization_id == self.organization.id

            when(
                'The organization not exist with this id',
                url_parameters=dict(id=100)
            )
            assert status == 404

            when(
                'Trying to pass using id is alphabetical',
                url_parameters=dict(id='not-integer')
            )
            assert status == 404

            when(
                'Trying to pass with not exist user',
                form=Update(email='not_exist_user@example.com')
            )
            assert status == 404

            when(
                'The email format is invalid',
                form=Update(email='example')
            )
            assert status == '701 Invalid Email Format'

            when(
                'Trying to pass without email parameter in form',
                form=Remove('email')
            )
            assert status == '701 Invalid Email Format'

            when(
                'The role format is invalid',
                form=Update(role='example')
            )
            assert status == '724 Invalid Role Value'

            when(
                'Trying to pass without role parameter in form',
                form=Remove('role')
            )
            assert status == '723 Role Not In Form'

            when(
                'The user already in this organization',
                form=Update(email=self.member2.email)
            )
            assert status == '623 Already In This Organization'

            self.logout()
            self.login(email=self.member2.email, password='123456')
            when(
                'The user is not the owner of the organization',
                form=Update(email=self.member2.email),
                authorization=self._authentication_token,
            )
            assert status == 403

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

