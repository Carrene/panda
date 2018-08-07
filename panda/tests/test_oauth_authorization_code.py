from panda.oauth.authorization_code import AuthorizationCode
from panda.tests.helpers import LocadApplicationTestCase


class TestAuthorizationCode(LocadApplicationTestCase):

    def test_authorization_code(self):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        authorization_code = AuthorizationCode(dict(a='1'))
        dump = authorization_code.dump()

        load = AuthorizationCode.load(dump.decode())
        assert 1 == 1

