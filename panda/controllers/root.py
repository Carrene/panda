from nanohttp import Controller, json
from restfulpy.controllers import RootController

import panda
from .availabilities import AvailabilitiesController
from .emails import EmailsController


class ApiV1(Controller):
    emails = EmailsController()
    availabilities = AvailabilitiesController()

    @json
    def version(self):
        return {
            'version': panda.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

