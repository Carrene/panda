import os

from bddrest.authoring import when, status, response

from panda.models import Member, Application
from panda.tests.helpers import LocalApplicationTestCase


class TestApplicationRevoke(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)
        session.flush()

        cls.application = Application(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            owner_id=member.id
        )
        session.add(cls.application)
        session.commit()

        cls.member1 = Member(
            email='member1@example.com',
            title='username1',
            password='123abcABC'
        )
        session.add(cls.member1)
        session.flush()

        cls.application.members.append(cls.member1)
        session.commit()

    def test_revoke_application(self):
        self.login(email='member1@example.com', password='123abcABC')

        with self.given(
            f'Revoke the authorization of a application using application id',
            f'/apiv1/applications/id:{self.application.id}',
            f'REVOKE',
        ):
            assert status == 200
            assert response.json['id'] == self.application.id

            when('Trying to pass with wrong id', url_parameters=dict(id=50))
            assert status == 400

            when(
                'Trying to pass with invalid the type id',
                url_parameters=dict(id='id')
            )
            assert status == 400

            when('Send request with form parameter', form=dict(param='param'))
            assert status == '707 Form Not Allowed'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

