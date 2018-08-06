import itsdangerous
from nanohttp import json, context, HTTPStatus, settings, validate
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from panda.models import Client


class AuthorizationCodeController(RestController):

    @authorize
    @validate(
        client_id=dict(required=('605 We don\'t recognize this client')),
        scope=dict(required=('606 Invalid scope'))
    )
    @json
    def create(self):
        # FIXME: This validation must be performed inside the validation
        # decorator.
        if context.form.keys():
            raise HTTPStatus('707 Form not allowed')

       # FIXME Temporarily set here!!!
        scopes = ['profile', 'email']

        scope = context.query.get('scope')
        state = context.query.get('state')

        for s in scope.split('+'):
           if s not in scopes:
               raise HTTPStatus('606 Invalid scope')

        client = DBSession.query(Client).\
            filter(Client.id == context.query.get('client_id')).one_or_none()
        if not client:
            raise HTTPStatus('605 We don\'t recognize this client')

        redirect_uri = context.query.get('redirect_uri')\
            if context.query.get('redirect_uri') else client.redirect_uri

        location = f'{redirect_uri}?clint_id={client.id}'

        if state:
            location = f'{location}&state={state}'

        serializer = itsdangerous.URLSafeTimedSerializer \
            (settings.authorization_code.secret)
        authorization_code = serializer.dumps(dict(
            scope=scope,
            member_id=context.identity.id,
            member_title=context.identity.payload['name'],
            email=context.identity.email,
            client_id=client.id,
            client_title=client.title,
            location=location
        ))

        return dict(authorizationCode=authorization_code)

