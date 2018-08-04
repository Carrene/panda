import itsdangerous
from nanohttp import json, context, HTTPFound, HTTPStatus, settings, validate
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from panda.models import Client


class AuthorizationCodeController(RestController):

    @authorize
    @validate(
        client_id=dict(required=(True, '605 We don\'t recognize this client')),
        scope=dict(required=(True, '606 Invalid scope'))
    )
    @json
    def create(self):
        # FIXME Temporarily set here!!!
        scopes = ['profile', 'email']

        scope = context.query.get('scope')
        state = context.query.get('state')
        redirect_uri = context.query.get('redirect_uri')

        # FIXME: This validation must be performed inside the validation
        # decorator.
        if context.form.keys():
            raise HTTPStatus('707 Form not allowed')

        if scope not in scopes:
            raise HTTPStatus('606 Invalid scope')

        client = DBSession.query(Client).\
            filter(Client.id == context.query.get('client_id')).one_or_none()
        if not client:
            raise HTTPStatus('605 We don\'t recognize this client')

        if not redirect_uri:
            redirect_uri = client.redirect_uri

        serializer = itsdangerous.URLSafeTimedSerializer \
            (settings.authorization_code.secret)
        code = serializer.dumps(dict(scope=scope))

        location = f'{redirect_uri}?clint_id={client.id}&' \
            f'scope={scope}&code={code}'

        if state:
            location = f'{location}&state={state}'

        raise HTTPFound(location)

