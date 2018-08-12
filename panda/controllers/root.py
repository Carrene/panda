from nanohttp import Controller, json
from restfulpy.controllers import RootController

import panda
from ..oauth.controllers import AuthorizationCodeController, \
    AccessTokenController
from .availabilities import AvailabilityController
from .client import ClientController
from .email import EmailController
from .member import MemberController
from .password import PasswordController
from .reset_password_token import ResetPasswordTokenController
from .token import TokenController


class ApiV1(Controller):
    emails = EmailController()
    members = MemberController()
    availabilities = AvailabilityController()
    tokens = TokenController()
    resetpasswordtokens = ResetPasswordTokenController()
    passwords = PasswordController()
    clients = ClientController()
    authorizationcodes = AuthorizationCodeController()
    accesstokens = AccessTokenController()

    @json
    def version(self):
        return {
            'version': panda.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

