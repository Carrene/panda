import time

import pytest
from nanohttp import settings, HTTPStatus

from panda.tests.helpers import LocalApplicationTestCase
from panda.tokens import RegistrationToken, ResetPasswordToken, \
    PhoneNumberActivationToken


class TestTokens(LocalApplicationTestCase):

    def test_reset_password_token(self):

        # Create reset password token using dump and load mothods
        payload = dict(a=1, b=2)
        reset_password_token = ResetPasswordToken(payload)
        dump = reset_password_token.dump()
        load = ResetPasswordToken.load(dump.decode())
        assert load.payload == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus('607 Malformed Token').__class__
        ):
            load = ResetPasswordToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus('609 Token Expired').__class__
        ):
            settings.reset_password.max_age = 0.3
            reset_password_token = ResetPasswordToken(payload)
            dump = reset_password_token.dump()
            time.sleep(1)
            load = ResetPasswordToken.load(dump.decode())

    def test_registration_token(self):

        # Create registeration token using dump and load mothods
        payload = dict(a=1, b=2)
        registration_token = RegistrationToken(payload)
        dump = registration_token.dump()
        load = RegistrationToken.load(dump.decode())
        assert load.payload == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus('607 Malformed Token').__class__
        ):
            load = RegistrationToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus('609 Token Expired').__class__
        ):
            settings.registration.max_age = 0.3
            registration_token = RegistrationToken(payload)
            dump = registration_token.dump()
            time.sleep(1)
            load = RegistrationToken.load(dump.decode())

    def test_phone_number_activation_token(self):

        # Create registeration token using dump and load mothods
        payload = dict(phoneNumber='+989351234567')
        activation_token = PhoneNumberActivationToken(payload)
        dump = activation_token.dump()
        load = PhoneNumberActivationToken.load(dump.decode())
        assert load.payload == payload

        # Trying to load token using bad signature token
        with pytest.raises(
            HTTPStatus('607 Malformed Token').__class__
        ):
            load = PhoneNumberActivationToken.load('token')

        # Trying to load token when token is expired
        with pytest.raises(
            HTTPStatus('609 Token Expired').__class__
        ):
            settings.phone.activation_token.max_age = 0.3
            activation_token = PhoneNumberActivationToken(payload)
            dump = activation_token.dump()
            time.sleep(1)
            load = PhoneNumberActivationToken.load(dump.decode())

