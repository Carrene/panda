import os

from bddrest.authoring import when, status, response

from panda.models import Member, Application

from .helpers import LocalApplicationTestCase


class TestApplicationRevoke(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        cls.session = cls.create_session(expire_on_commit=True)
        owner1 = Member(
            email='owner1@example.com',
            password='123abcABC',
            title='owner1',
            first_name='owner_first_name',
            last_name='owner_last_name',
            role='member'
        )
        owner2 = Member(
            email='owner2@example.com',
            title='owner2',
            first_name='owner_first_name',
            last_name='owner_last_name',
            password='123abcABC',
            role='member'
        )
        member1 = Member(
            email='member1@example.com',
            title='username1',
            first_name='member1_first_name',
            last_name='member1_last_name',
            password='123abcABC',
            role='member'
        )
        member2 = Member(
            email='member2@example.com',
            title='username2',
            first_name='member2_first_name',
            last_name='member2_last_name',
            password='123abcABC',
            role='member'
        )
        member3 = Member(
            email='member3@example.com',
            title='username3',
            first_name='member3_first_name',
            last_name='member3_last_name',
            password='123abcABC',
            role='member'
        )
        cls.application1 = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner=owner1,
            members=[member1, member2, member3]
        )
        cls.application2 = Application(
            title='oauth',
            redirect_uri='http://example2.com/oauth2',
            secret=os.urandom(32),
            owner=owner2,
            members=[member3]
        )

        cls.session.add(cls.application1)
        cls.session.add(cls.application2)
        cls.session.commit()

    def test_revoke_application(self):
        self.login(email='owner1@example.com', password='123abcABC')

        with self.given(
            f'Revoke the authorized application using the application id',
            f'/apiv1/applications/id:{self.application1.id}',
            f'REVOKE',
        ):
            assert status == 200
            assert response.json['id'] == self.application1.id
            assert len(self.application1.members) == 0
            assert len(self.application2.members) == 1

            when(
                'The member isn\'t the owner of the application',
                url_parameters=dict(id=self.application2.id)
            )
            assert status == 404

            when('Trying to pass with wrong id', url_parameters=dict(id=0))
            assert status == 404

            when('Type of the id is invalid', url_parameters=dict(id='id'))
            assert status == 404

            when('Send request with form parameter', form=dict(param='param'))
            assert status == '707 Form Not Allowed'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

