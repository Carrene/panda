import time

import pytest
from nanohttp import settings, HTTPStatus

from panda.oauth.tokens import AccessToken, AuthorizationCode
from panda.tokens import RegisterationToken, ResetPasswordToken
from panda.tests.helpers import LocadApplicationTestCase


class TestOauthTokens(LocadApplicationTestCase):

    def test_reset_password_token(self):

        # Create reset password token using dump and load mothods
        payload = dict(a=1, b=2)
        reset_password_token = ResetPasswordToken(payload)
        dump = reset_password_token.dump()
        load = ResetPasswordToken.load(dump.decode())

        assert load == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus(status='607 Malformed token').__class__
        ):
            load = ResetPasswordToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus(status='609 Token expired').__class__
        ):
            settings.reset_password.max_age = 0.3
            reset_password_token = ResetPasswordToken(payload)
            dump = reset_password_token.dump()
            time.sleep(1)
            load = ResetPasswordToken.load(dump.decode())

    def test_registeration_token(self):

        # Create registeration token using dump and load mothods
        payload = dict(a=1, b=2)
        registeration_token = RegisterationToken(payload)
        dump = registeration_token.dump()
        load = RegisterationToken.load(dump.decode())

        assert load == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus(status='607 Malformed token').__class__
        ):
            load = RegisterationToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus(status='609 Token expired').__class__
        ):
            settings.registeration.max_age = 0.3
            registeration_token = RegisterationToken(payload)
            dump = registeration_token.dump()
            time.sleep(1)
            load = RegisterationToken.load(dump.decode())

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
        with pytest.raises(
            HTTPStatus(status='609 Token expired').__class__
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

        assert load == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus(status='607 Malformed authorization code').__class__
        ):
            load = AuthorizationCode.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus(status='609 Token expired').__class__
        ):
            settings.authorization_code.max_age = 0.3
            authorization_code = AuthorizationCode(payload)
            dump = authorization_code.dump()
            time.sleep(1)
            load = AuthorizationCode.load(dump.decode())

