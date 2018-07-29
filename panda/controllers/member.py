import itsdangerous
from nanohttp import json, context, settings, HTTPStatus
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from panda.models import Member
from panda.validators import title_validator, password_validator


class MemberController(ModelRestController):

    @json
    @commit
    @title_validator
    @password_validator
    def register(self):
        title = context.form.get('title')
        password = context.form.get('password')
        ownership_token = context.form.get('ownership_token')

        if DBSession.query(Member.title).filter(Member.title == title).count():
            raise HTTPStatus('604 Title is already registered')

        serializer = \
            itsdangerous.URLSafeTimedSerializer(settings.registeration.secret)

        try:
             email = serializer.loads(
                ownership_token,
                max_age=settings.registeration.max_age
            )

        except itsdangerous.BadSignature:
            raise HTTPStatus(status='704 Invalid token')

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus('601 Email address is already registered')

        member = Member(email=email, title=title, password=password)

        DBSession.add(member)

        principal = member.create_jwt_principal()
        context.response_headers.add_header(
            'X-New-JWT-Token',
            principal.dump().decode('utf-8')
        )

        return member

