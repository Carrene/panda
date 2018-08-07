import itsdangerous
from nanohttp import json, context, HTTPStatus, settings, validate
from restfulpy.authorization import authorize
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from panda.models import Client


class AccessTokenController(RestController):

    @validate(
        client_id=dict(required='708 Client id not in form'),
        secret=dict(required='710 Secret not in form'),
        code=dict(required='708 Code not in form')
    )
    @json
    def create(self):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        code = context.form.get('code')

        serializer = itsdangerous. \
            URLSafeTimedSerializer(settings.authorization_code.secret)
        try:
             authorization_code = serializer.loads(
                code,
                max_age=settings.authorization_code.max_age
            )

        except itsdangerous.BadSignature:
            raise HTTPStatus(status='607 Malformed authorization code')

        client = DBSession.query(Client).\
            filter(Client.id == context.form.get('client_id')).one_or_none()
        if not client:
            raise HTTPStatus('605 We don\'t recognize this client')

        if not client.validate_secret(context.form.get('secret')):
            raise HTTPStatus('608 Malformed secret')


        return dict()

