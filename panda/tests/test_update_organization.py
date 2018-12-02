import io
from os.path import dirname, abspath, join

from bddrest.authoring import when, status, response
from nanohttp import settings

from panda.models import Member, Organization, OrganizationMember
from panda.tests.helpers import LocalApplicationTestCase


TEST_DIR = abspath(dirname(__file__))
STUFF_DIR = join(TEST_DIR, 'stuff')
VALID_LOGO_PATH = join(STUFF_DIR, 'logo-150x150.jpg')
INVALID_FORMAT_LOGO_PATH = join(STUFF_DIR, 'test.pdf')
INVALID_MAXIMUM_SIZE_LOGO_PATH = join(STUFF_DIR, 'logo-550x550.jpg')
INVALID_MINIMUM_SIZE_LOGO_PATH = join(STUFF_DIR, 'logo-50x50.jpg')
INVALID_RATIO_LOGO_PATH = join(STUFF_DIR, 'logo-150x100.jpg')
INVALID_MAXMIMUM_LENGTH_LOGO_PATH = join(
    STUFF_DIR,
    'logo-maximum-length.jpg'
)


class TestOrganization(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        member1 = Member(
            email='user1@example.com',
            title='user1',
            password='123456',
            role='member'
        )
        session.add(member1)

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

        cls.organization1 = Organization(
            title='organization1',
        )
        session.add(cls.organization1)
        session.flush()

        organization_member1 = OrganizationMember(
            organization_id=cls.organization1.id,
            member_id=member1.id,
            role='owner',
        )
        session.add(organization_member1)

        organization2 = Organization(
            title='organization2',
        )
        session.add(organization2)
        session.flush()

        organization_member2 = OrganizationMember(
            organization_id=organization2.id,
            member_id=member1.id,
            role='owner',
        )
        session.add(organization_member2)

        organization_member3 = OrganizationMember(
            member_id=cls.member2.id,
            organization_id=cls.organization1.id,
            role='member',
        )
        session.add(organization_member3)
        session.commit()

    def test_update_organization(self):
        title = 'My-organization'
        url = 'www.example.com'
        domain = 'example.com'
        self.login(email='user1@example.com', password='123456')

        with self.given(
            f'The organization has successfully updated',
            f'/apiv1/organizations/id:{self.organization1.id}',
            f'UPDATE',
            multipart=dict(
                title=title,
                url=url,
                domain=domain,
            )
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['logo'] is None
            assert response.json['url'] == url
            assert response.json['domain'] == domain

            when(
                'The organization title is exist',
                multipart=dict(title='organization2')
            )
            assert status == '622 Organization Title Is Already Taken'

            when(
                'The title format is invalid',
                multipart=dict(title='my organ')
            )
            assert status == 705

            when(
                'The length of title is too long',
                multipart=dict(title=(40 + 1) * 'a')
            )
            assert status == 720

            when(
                'The URL format is invalid',
                multipart=dict(url='example.com')
            )
            assert status == '725 Invalid URL Format'

            when(
                'The domain format is invalid',
                multipart=dict(domain='example')
            )
            assert status == '726 Invalid Domain Format'

            when('Trying to pass with empty multipart', multipart={})
            assert status == '400 Empty Form'

            with open(VALID_LOGO_PATH, 'rb') as f:
                when(
                    'Updating the logo of organization',
                    multipart=dict(logo=io.BytesIO(f.read()))
                )
                assert response.json['logo'].startswith(
                    settings.storage.base_url
                )

            with open(INVALID_MAXIMUM_SIZE_LOGO_PATH, 'rb') as f:
                when(
                    'The logo size is exceeded the maximum size',
                    multipart=dict(logo=io.BytesIO(f.read()))
                )
                assert status == 618

            with open(INVALID_MINIMUM_SIZE_LOGO_PATH, 'rb') as f:
                when(
                    'The logo size is less than minimum size',
                    multipart=dict(logo=io.BytesIO(f.read()))
                )
                assert status == 618

            with open(INVALID_RATIO_LOGO_PATH, 'rb') as f:
                when(
                    'Aspect ratio of the logo is invalid',
                    multipart=dict(logo=io.BytesIO(f.read()))
                )
                assert status == 619

            with open(INVALID_FORMAT_LOGO_PATH, 'rb') as f:
                when(
                    'Format of the logo is invalid',
                    multipart=dict(logo=io.BytesIO(f.read()))
                )
                assert status == 620

            with open(INVALID_MAXMIMUM_LENGTH_LOGO_PATH, 'rb') as f:
                when(
                    'The maxmimum length of logo is invalid',
                    multipart=dict(logo=io.BytesIO(f.read()))
                )
                assert status == 621

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

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

            self.logout()
            self.login(self.member2.email, '123456')
            when(
                'The member is not owner of the organization',
                url_parameters=dict(id=self.member2.id),
                authorization=self._authentication_token
            )
            assert status == 404

            self.login(self.member3.email, '123456')
            when(
                'The user not member of organization',
                url_parameters=dict(id=self.member3.id),
                authorization=self._authentication_token
            )
            assert status == 404

