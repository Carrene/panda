from nanohttp import json, context
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession

from ..models import Application, ApplicationMember


class AuthorizedApplicationController(ModelRestController):
    __model__ = Application

    @authorize
    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    def list(self):
        application = DBSession.query(Application) \
            .filter(ApplicationMember.member_id == context.identity.id)
        return application

