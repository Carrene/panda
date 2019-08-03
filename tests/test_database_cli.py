from .helpers import LocalApplicationTestCase
from panda.models import Member, Application


class TestDatabaseCLI(LocalApplicationTestCase):

    def test_basedata(self):
        self.__application__.insert_basedata()
        session = self.create_session()

        assert session.query(Member).count() == 1
        assert session.query(Member).filter(Member.title == 'GOD').one()

        assert session.query(Application).count() == 1
        assert session.query(Application) \
            .filter(Application.title == 'oauth') \
            .one()

    def test_mockup(self):
        self.__application__.insert_mockup()
        session = self.create_session()

        assert session.query(Member).count() == 10

