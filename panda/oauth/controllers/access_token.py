from nanohttp import json, context, HTTPStatus, validate
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from .. import AccessToken, AuthorizationCode
from ...models import Client


class AccessTokenController(RestController):

    @json(prevent_empty_form=True)
    @validate(
        clientId=dict(required='708 Client Id Not In Form'),
        secret=dict(required='710 Secret Not In Form'),
        code=dict(required='709 Code Not In Form')
    )
    def create(self):
        authorization_code = AuthorizationCode.load(context.form.get('code'))

        client = DBSession.query(Client) \
            .filter(Client.id == context.form.get('clientId')) \
            .one_or_none()
        if not client:
            raise HTTPStatus('605 We Don\'t Recognize This Client')

        if not client.validate_secret(context.form.get('secret')):
            raise HTTPStatus('608 Malformed Secret')

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

