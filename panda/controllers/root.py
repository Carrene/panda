from nanohttp import Controller, json
from restfulpy.controllers import RootController

import panda
from ..oauth.controllers import AuthorizationCodeController, \
    AccessTokenController
from .availabilities import AvailabilityController
from .application import ApplicationController
from .email import EmailController
from .member import MemberController
from .password import PasswordController
from .reset_password_token import ResetPasswordTokenController
from .token import TokenController
from .my_application import MyApplicationController
from .authorized_application import AuthorizedApplicationController
from .phones import PhoneNumberActivationTokenController, PhoneNumberController


class ApiV1(Controller):
    emails = EmailController()
    members = MemberController()
    availabilities = AvailabilityController()
    tokens = TokenController()
    resetpasswordtokens = ResetPasswordTokenController()
    passwords = PasswordController()
    applications = ApplicationController()
    authorizationcodes = AuthorizationCodeController()
    accesstokens = AccessTokenController()
    myapplications = MyApplicationController()
    authorizedapplications = AuthorizedApplicationController()
    phonenumberactivationtokens = PhoneNumberActivationTokenController()
    phonenumbers = PhoneNumberController()

    @json
    def version(self):
        return {
            'version': panda.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

