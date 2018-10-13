from bddrest.authoring import status, response, Update, Remove, when

from panda.models import Member
from panda.tests.helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.member = Member(
            email='user1@example.com',
            title='member_title',
            password='123456',
            role='member'
        )
        session.add(cls.member)
        session.commit()

    def test_update_name(self):
        self.login(email=self.member.email, password='123456')

        with self.given(
            'Updating name of member',
            '/apiv1/members',
            'UPDATE',
            form=dict(name='username')
        ):
            assert status == 200
            assert response.json['id'] == self.member.id
            assert response.json['name'] == 'username'

            when('Trying to pass without name parameter', form=Remove('name'))
            assert response.json['id'] == self.member.id
            assert response.json['name'] == 'username'

            when('The name have numbers', form=Update(name='name1'))
            assert status == '716 Invalid Format Name'

            when('Invalid the min lenght of name', form=Update(name='n'))
            assert status == '716 Invalid Format Name'

            when(
                'Invalid the max lenght of name',
                form=Update(name='name name name name n')
            )
            assert status == '716 Invalid Format Name'

            when(
                'Trying to pass with redundant parameters in form',
                form=Update(title='title')
            )
            assert status == '717 Invalid Field, Only The Name Parameter ' \
                'Accepted'

            when('Trying with an unauthorized member', authorization=None)
            assert status == 401

