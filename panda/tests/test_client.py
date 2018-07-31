from bddrest.authoring import Update, Remove, when, status, response

from panda.models import Member
from panda.tests.helpers import LocadApplicationTestCase


class TestClient(LocadApplicationTestCase):

    @classmethod
    def mockup(cls):
        member = Member(
            email='already.added@example.com',
            title='username',
            password='123abcABC'
        )
        session = cls.create_session()
        session.add(member)
        session.commit()

    def test_define_client(self):
        self.login(
            email='already.added@example.com',
            password='123abcABC',
            url='/apiv1/tokens',
            verb='CREATE'
        )

        title = 'example_client'
        redirect_uri = 'http://example.com/oauth2'

        with self.given(
            'The client has successfully defined',
            '/apiv1/clients',
            'define',
            form=dict(
                title=title,
                redirect_uri=redirect_uri
            )
        ):
            assert status == 200
            assert response.json['title'] == title
            assert response.json['redirect_uri'] == redirect_uri
            assert 'secret' in response.json

            when('Trying to pass with balnk title', form=Update(title=' '))
            assert status == '705 Invalid title format'

            when(
                'Trying to pass without title parameter',
                form=Remove('title')
            )
            assert status == '705 Invalid title format'

            when(
                'Trying to pass with balnk title',
                form=Update(redirect_uri=' ')
            )
            assert status == '706 Redirect uri is blank'

            when(
                'Trying to pass without title parameter',
                form=Remove('redirect_uri')
            )
            assert status == '706 Redirect uri is blank'

            self.logout()
            import pudb; pudb.set_trace()  # XXX BREAKPOINT
            when('Trying to pass unathorized member')
            assert status == 401

