from bddrest.authoring import when, status, response, Remove, given

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
        session.add(member)

        organization = Organization(
            name='organization-name',
            members=[member],
        )
        session.add(organization)
        session.commit()

    def test_create_organization(self):
        name = 'My-organization'
        self.login(email='already.added@example.com', password='123abcABC')

        with self.given(
            'The organization has successfully created',
            '/apiv1/organizations',
            'CREATE',
            form=dict(name=name)
        ):
            assert status == 200
            assert response.json['name'] == name

            when(
                'The organization name is exist',
                form=dict(name='organization-name')
            )
            assert status == '622 Organization Name Is Already Taken'

            when('The name format is invalid', form=dict(name='my organ'))
            assert status == 721

            when('The length name is too long', form=dict(name=(40 + 1) * 'a'))
            assert status == 720

            when('The name not in form', form=given - 'name' + dict(a='a'))
            assert status == 718

            when('Trying to pass with empty form', form=Remove('name'))
            assert status == '400 Empty Form'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

