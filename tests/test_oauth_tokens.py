import time

import pytest
from nanohttp import settings, HTTPStatus

from panda.oauth.tokens import AccessToken, AuthorizationCode

from .helpers import LocalApplicationTestCase


class TestOauthTokens(LocalApplicationTestCase):

    def test_access_token(self):

        # Create access token using dump and load methods
        payload = dict(a=1, b=2)
        access_token = AccessToken(payload)
        dump = access_token.dump()
        load = AccessToken.load(dump.decode())
        assert load.payload == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus('607 Malformed access token').__class__
        ):
            load = AccessToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus('609 Token expired').__class__
        ):
            settings.access_token.max_age = 0.3
            access_token = AccessToken(payload)
            dump = access_token.dump()
            time.sleep(1)
            load = AccessToken.load(dump.decode())

    def test_authorization_code(self):

        # Create authorization code using dump and load mothods
        payload = dict(a=1, b=2)
        authorization_code = AuthorizationCode(payload)
        dump = authorization_code.dump()
        load = AuthorizationCode.load(dump.decode())
        assert load.payload == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus('607 Malformed authorization code').__class__
        ):
            load = AuthorizationCode.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus('609 Token expired').__class__
        ):
            settings.authorization_code.max_age = 0.3
            authorization_code = AuthorizationCode(payload)
            dump = authorization_code.dump()
            time.sleep(1)
            load = AuthorizationCode.load(dump.decode())

