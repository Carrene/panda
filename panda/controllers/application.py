import hashlib

from nanohttp import json, context, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from .. import cryptohelpers
from ..models import Application


class ApplicationController(ModelRestController):
    __model__ = Application

    @json(prevent_empty_form=True)
    @authorize
    @Application.expose
    @commit
    def define(self):
        title = context.form.get('title')
        redirect_uri = context.form.get('redirectUri')

        if not title or title.isspace():
            raise HTTPStatus('705 Invalid Title Format')

        if not redirect_uri or redirect_uri.isspace():
            raise HTTPStatus('706 Redirect URI Is Blank')

        application = Application(
            title=title,
            redirect_uri=redirect_uri,
            member_id=context.identity.id
        )
        application.secret = hashlib.pbkdf2_hmac(
            'sha256',
            str(context.identity.id).encode(),
            cryptohelpers.random(32),
            100000,
            dklen=32
        )
        DBSession.add(application)
        return application
