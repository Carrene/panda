from nanohttp import json, context, HTTPStatus, HTTPNotFound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit
from sqlalchemy_media import store_manager

from ..models import Member
from ..tokens import RegisterationToken
from ..validators import title_validator, password_validator, member_validator


class MemberController(ModelRestController):
    __model__ = Member

    @json(prevent_empty_form=True)
    @title_validator
    @password_validator
    @Member.expose
    @commit
    def register(self):
        title = context.form.get('title')
        password = context.form.get('password')
        ownership_token = context.form.get('ownershipToken')
        regiteration_token_principal = RegisterationToken.load(ownership_token)
        email = regiteration_token_principal.email

        if DBSession.query(Member.title).filter(Member.title == title).count():
            raise HTTPStatus('604 Title Is Already Registered')

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPStatus('601 Email Address Is Already Registered')

        member = Member(
            email=email,
            title=title,
            password=password,
            role='member'
        )
        DBSession.add(member)
        DBSession.flush()
        principal = member.create_jwt_principal()
        context.response_headers.add_header(
            'X-New-JWT-Token',
            principal.dump().decode('utf-8')
        )
        return member

    @authorize
    @json
    @Member.expose
    def get(self, id):
        id = context.identity.id if id == 'me' else id
        try:
            id = int(id)
        except(ValueError, TypeError):
            raise HTTPNotFound()

        member = DBSession.query(Member).get(id)
        if not member:
            raise HTTPNotFound()

        if member.id != context.identity.id:
            context.identity.assert_roles('admin')

        return member

    @store_manager(DBSession)
    @authorize
    @member_validator
    @json(
        form_whitelist=(
            ['name', 'avatar'],
            '717 Invalid Field, Only The Name And Avatar Parameters Are ' \
            'Accepted'
        ),
        prevent_empty_form=True
    )

    @Member.expose
    @commit
    def update(self):
        member = DBSession.query(Member).get(context.identity.id)
        member.update_from_request()
        return member

