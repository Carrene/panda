import time

import pytest
from nanohttp import settings, HTTPStatus

from panda.oauth.access_token import AccessToken
from panda.tests.helpers import LocadApplicationTestCase


class TestAccessToken(LocadApplicationTestCase):

    def test_access_token(self):

        # Create access token using dump and load methods
        payload = dict(a=1, b=2)
        access_token = AccessToken(payload)
        dump = access_token.dump()
        load = AccessToken.load(dump.decode())

        assert load == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus(status='607 Malformed access token').__class__
        ):
            load = AccessToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(HTTPStatus(status='609 Token expired').__class__):

            settings.access_token.max_age = 0.3
            access_token = AccessToken(payload)
            dump = access_token.dump()
            time.sleep(1)
            load = AccessToken.load(dump.decode())

