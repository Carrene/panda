import itsdangerous
from nanohttp import json, context, validate, settings, HTTPStatus
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from panda.models import Member, RegisterEmail


class EmailsController(ModelRestController):

    @commit
    @json
    @validate(
        email=dict(
            required=(True, '701 Invalid email format'),
            pattern=(
                '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                '701 Invalid email format'
            )
        )
    )
    def claim(self):
        email = context.form.get('email')

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus(
                '601 Email address is already registered'
            )

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.activation.secret)

        token = serializer.dumps(email)

        DBSession.add(
            RegisterEmail(
                to=email,
                subject='Register your CAS account',
                body={
                    'register_token': token,
                    'register_url': settings.activation.url
                }
            )
        )

        return dict(email=email)

