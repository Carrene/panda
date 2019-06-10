from nanohttp import json, context, HTTPNotFound, validate, int_or_notfound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit
from sqlalchemy_media import store_manager

from ..exceptions import HTTPEmailAddressAlreadyRegistered, \
    HTTPTitleAlreadyRegistered
from ..models import Member
from ..tokens import RegistrationToken
from ..validators import member_register_validator, member_update_validator


class MemberController(ModelRestController):
    __model__ = Member

    @json(prevent_empty_form=True)
    @member_register_validator
    @commit
    def register(self):
        title = context.form.get('title')
        password = context.form.get('password')
        ownership_token = context.form.get('ownershipToken')
        regitration_token_principal = RegistrationToken.load(ownership_token)
        email = regitration_token_principal.email

        if DBSession.query(Member.title).filter(Member.title == title).count():
            raise HTTPTitleAlreadyRegistered()

        if DBSession.query(Member.email).filter(Member.email == email).count():
            raise HTTPEmailAddressAlreadyRegistered()

        member = Member(
            email=email,
            title=title,
            password=password,
            name=context.form.get('name'),
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
        id = context.identity.reference_id if id == 'me' else id
        id = int_or_notfound(id)

        member = DBSession.query(Member).get(id)
        if not member:
            raise HTTPNotFound()

        if member.id != context.identity.reference_id:
            context.identity.assert_roles('admin')

        return member

    @store_manager(DBSession)
    @authorize
    @json(
        form_whitelist=(
            ['name', 'avatar'],
            '717 Invalid field, only the name and avatar parameters are ' \
            'accepted'
        ),
        prevent_empty_form=True
    )
    @member_update_validator
    @Member.expose
    @commit
    def update(self, id):
        id = int_or_notfound(id)

        member = DBSession.query(Member).get(id)
        if member is None:
            raise HTTPNotFound()

        if member.id != context.identity.reference_id:
            raise HTTPNotFound()

        member.update_from_request()
        context.application.__authenticator__.invalidate_member(member.id)
        return member

