from os.path import abspath, dirname, join

from nanohttp import Controller, json, Static, settings
from restfulpy.controllers import RootController

import panda
from ..oauth.controllers import AuthorizationCodeController, \
    AccessTokenController
from .applications import ApplicationController, MyApplicationController,\
    AuthorizedApplicationController
from .availabilities import AvailabilityController
from .email import EmailController
from .member import MemberController
from .passwords import PasswordController, ResetPasswordTokenController
from .phones import PhoneNumberActivationTokenController, PhoneNumberController
from .token import TokenController
from .organizations import OrganizationController


here = abspath(dirname(__file__))
avatar_storage = abspath(join(here, '../..', 'data/assets'))


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
    organizations = OrganizationController()

    @json
    def version(self):
        return {
            'version': panda.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()
    assets = Static(avatar_storage)

