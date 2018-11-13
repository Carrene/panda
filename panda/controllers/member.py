from nanohttp import json, context, HTTPStatus, HTTPNotFound, validate
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
    @validate(
        ownershipToken=dict(
            required='727 Token Not In Form',
        )
    )
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
        context.application.__authenticator__.setup_response_headers(principal)
        return member

    @store_manager(DBSession)
    @authorize
    @json
    @Member.expose
    def get(self, id):
        id = context.identity.id if id == 'me' else id
        try:
            id = int(id)
        except (ValueError, TypeError):
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
            '717 Invalid field, only the name and avatar parameters are ' \
            'accepted'
        ),
        prevent_empty_form=True
    )
    @Member.expose
    @commit
    def update(self, id):
        try:
            id = int(id)
        except (ValueError, TypeError):
            raise HTTPNotFound()

        member = DBSession.query(Member).get(id)
        if member is None:
            raise HTTPNotFound()

        if member.id != context.identity.reference_id:
            raise HTTPNotFound()

        member.update_from_request()
        context.application.__authenticator__.invalidate_member(member.id)
        return member

