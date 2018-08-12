from nanohttp import json, context, HTTPStatus, validate
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from ...models import Client
from .. import AccessToken, AuthorizationCode


class AccessTokenController(RestController):

    @validate(
        client_id=dict(required='708 Client id not in form'),
        secret=dict(required='710 Secret not in form'),
        code=dict(required='708 Code not in form')
    )
    @json
    def create(self):
        authorization_code = AuthorizationCode.load(context.form.get('code'))

        client = DBSession.query(Client) \
            .filter(Client.id == context.form.get('client_id')) \
            .one_or_none()
        if not client:
            raise HTTPStatus('605 We don\'t recognize this client')

        if not client.validate_secret(context.form.get('secret')):
            raise HTTPStatus('608 Malformed secret')

        access_token_payload = dict(
            client_id=client.id,
            member_id=authorization_code['memberId'],
            scope=authorization_code['scope'],
        )
        access_token = AccessToken(access_token_payload)
        return dict(access_token=access_token.dump())

