from nanohttp import json, context, HTTPStatus, validate
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from .. import AccessToken, AuthorizationCode
from ...models import Client


class AccessTokenController(RestController):

    @json(prevent_empty_form=True)
    @validate(
        clientId=dict(required='708 Client id not in form'),
        secret=dict(required='710 Secret not in form'),
        code=dict(required='709 Code not in form')
    )
    def create(self):
        authorization_code = AuthorizationCode.load(context.form.get('code'))

        client = DBSession.query(Client) \
            .filter(Client.id == context.form.get('clientId')) \
            .one_or_none()
        if not client:
            raise HTTPStatus('605 We don\'t recognize this client')

        if not client.validate_secret(context.form.get('secret')):
            raise HTTPStatus('608 Malformed secret')

        access_token_payload = dict(
            clientId=client.id,
            memberId=authorization_code['memberId'],
            scopes=authorization_code['scopes'],
        )
        access_token = AccessToken(access_token_payload)
        return dict(
            accessToken=access_token.dump(),
            memberId=authorization_code['memberId']
        )

