from nanohttp import Controller, json
from restfulpy.controllers import RootController

import panda
from .emails import EmailsController


class ApiV1(Controller):

    emails = EmailsController()

    @json
    def version(self):
        return {
            'version': panda.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

