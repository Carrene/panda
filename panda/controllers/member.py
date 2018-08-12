from nanohttp import json, context, HTTPStatus, action
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..tokens import RegisterationToken
from ..models import Member
from ..validators import title_validator, password_validator


class MemberController(ModelRestController):
    __model__ = Member

    @action(prevent_empty_form=True)
    @title_validator
    @password_validator
    @json
    @Member.expose
    @commit
    def register(self):
        title = context.form.get('title')
        password = context.form.get('password')
        ownership_token = context.form.get('ownershipToken')

        if DBSession.query(Member.title).filter(Member.title == title).count():
            raise HTTPStatus('604 Title is already registered')

        regiteration_token_payload = RegisterationToken.load(ownership_token)
        email = regiteration_token_payload['email']

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

