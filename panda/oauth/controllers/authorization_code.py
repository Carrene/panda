from nanohttp import json, context, HTTPStatus, validate, action
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from ...models import Client
from .. import AuthorizationCode


class AuthorizationCodeController(RestController):

    @action(prevent_form='707 Form not allowed')
    @authorize
    @validate(
        client_id=dict(required='605 We don\'t recognize this client'),
        scope=dict(required='606 Invalid scope')
    )
    @json
    def create(self):

       # FIXME Temporarily set here!!!
        scopes = ['profile', 'email']

        scope = context.query.get('scope')
        state = context.query.get('state')

        for s in scope.split('+'):
            if s not in scopes:
                raise HTTPStatus('606 Invalid scope')

        client = DBSession.query(Client) \
            .filter(Client.id == context.query.get('client_id')) \
            .one_or_none()
        if not client:
            raise HTTPStatus('605 We don\'t recognize this client')

        redirect_uri = context.query.get('redirect_uri')\
            if context.query.get('redirect_uri') else client.redirect_uri

        location = f'{redirect_uri}?clint_id={client.id}'

        if state:
            location = f'{location}&state={state}'

        authorization_code_payload = dict(
            scope=scope,
            memberId=context.identity.id,
            memberTitle=context.identity.payload['name'],
            email=context.identity.email,
            clientId=client.id,
            clientTitle=client.title,
            location=location
        )
        authorization_code = AuthorizationCode(authorization_code_payload)
        return dict(authorizationCode=authorization_code.dump())

