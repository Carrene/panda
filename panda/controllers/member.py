from nanohttp import json, context, HTTPStatus, HTTPForbidden
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit

from ..models import Member
from ..tokens import RegisterationToken
from ..validators import title_validator, password_validator
from ..oauth.tokens import AccessToken


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

    @json(prevent_form='400 Form Not Allowed')
    def get(self, id):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT

        if not isinstance(context.identity, AccessToken):
            raise HTTPForbidden()

        if id != context.identity.payload['member_id']:
            raise HTTPForbidden()

        return {}
