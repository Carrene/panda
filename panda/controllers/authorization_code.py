from nanohttp import json
from restfulpy.orm import commit


class AuthorizationCodeController(RestController):

    @json
    @commit
    def get(self, client_id, scope, state, redirect_uri):

        return dict()

