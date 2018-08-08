import time

import pytest
from nanohttp import settings, HTTPStatus

from panda.oauth.authorization_code import AuthorizationCode
from panda.tests.helpers import LocadApplicationTestCase


class TestAuthorizationCode(LocadApplicationTestCase):

    def test_authorization_code(self):

        # Create authorization code using dump and load mothods
        payload = dict(a=1, b=2)
        authorization_code = AuthorizationCode(payload)
        dump = authorization_code.dump()
        load = AuthorizationCode.load(dump.decode())

        assert load == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus(status='607 Malformed authorization code').__class__
        ):
            load = AuthorizationCode.load('token')

        # Trying to load token when token is expired
        with pytest.raises(HTTPStatus(status='609 Token expired').__class__):

            settings.authorization_code.max_age = 0.3
            authorization_code = AuthorizationCode(payload)
            dump = authorization_code.dump()
            time.sleep(1)
            load = AuthorizationCode.load(dump.decode())

