import hashlib

from nanohttp import json, context, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from .. import cryptohelpers
from ..models import Client


class ClientController(ModelRestController):
    __model__ = Client

    @json(prevent_empty_form=True)
    @authorize
    @Client.expose
    @commit
    def define(self):
        title = context.form.get('title')
        redirect_uri = context.form.get('redirectUri')

        if not title or title.isspace():
            raise HTTPStatus('705 Invalid title format')

        if not redirect_uri or redirect_uri.isspace():
            raise HTTPStatus('706 Redirect uri is blank')

        client = Client(
            title=title,
            redirect_uri=redirect_uri,
            member_id=context.identity.id
        )
        client.secret = hashlib.pbkdf2_hmac(
            'sha256',
            str(context.identity.id).encode(),
            cryptohelpers.random(32),
            100000,
            dklen=32
        )
        DBSession.add(client)
        return client

