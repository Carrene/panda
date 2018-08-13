import os
import base64

from bddrest.authoring import status, response

from panda.models import Member, Client
from panda.tests.helpers import LocadApplicationTestCase


class TestMemberProfile(LocadApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cls.member = Member(
            email='member@example.com',
            title='member_title',
            password='123abcABC'
        )
        session.add(cls.member)
        session.flush()

        cls.client = Client(
            title='oauth',
            redirect_uri='http://example1.com/oauth2',
            secret=os.urandom(32),
            member_id=cls.member.id
        )
        session.add(cls.client)
        session.commit()

    def test_member_profile(self):
        self.login(
            email=self.member.email,
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        with self.given(
            'Create authorization code',
            '/apiv1/authorizationcodes',
            'CREATE',
            query=dict(
                client_id=self.client.id,
                scope='profile',
                state='123456',
                redirect_uri='http://example2.com/oauth2'
            )
        ):
            authorization_code = response.json['authorizationCode']

        with self.given(
            'Create access token',
            '/apiv1/accesstokens',
            'CREATE',
            form=dict(
                client_id=self.client.id,
                secret=base64.encodebytes(self.client.secret),
                code=authorization_code,
            )
        ):
            assert status == 200
            access_token = response.json['access_token']

        self.logout()

        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        with self.given(
            'Get member profile',
            f'/apiv1/members/id:{self.member.id}',
            'GET',
            headers={'authorization': f'oauth2-accesstoken {access_token}'}
        ):
            assert status == 200

