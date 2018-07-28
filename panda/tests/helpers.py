from restfulpy.testing import ApplicableTestCase

from panda import Panda
from panda.models import Member


class LoadApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda

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

