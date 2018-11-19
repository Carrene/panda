from nanohttp import json, context, validate
from restfulpy.controllers import RestController
from restfulpy.orm import DBSession

from .. import AccessToken, AuthorizationCode
from ...exceptions import HTTPUnRecognizedApplication, HTTPMalformedSecret
from ...models import Application, ApplicationMember


class AccessTokenController(RestController):

    @json(prevent_empty_form=True)
    @validate(
        applicationId=dict(required='708 Application Id Not In Form'),
        secret=dict(required='710 Secret Not In Form'),
        code=dict(required='709 Code Not In Form')
    )
    def create(self):
        authorization_code = AuthorizationCode.load(context.form.get('code'))

        application = DBSession.query(Application) \
            .filter(Application.id == context.form.get('applicationId')) \
            .one_or_none()
        if not application:
            raise HTTPUnRecognizedApplication()

        if not application.validate_secret(context.form.get('secret')):
            raise HTTPMalformedSecret()

        application_member = DBSession.query(ApplicationMember) \
            .filter(
                ApplicationMember.application_id == application.id,
                ApplicationMember.member_id == authorization_code.member_id
            ) \
            .one_or_none()

        if not application_member:
            application_member = ApplicationMember(
                application_id=application.id,
                member_id=authorization_code.member_id
            )
            DBSession.add(application_member)
            DBSession.flush()

        access_token_payload = dict(
            applicationId=application.id,
            memberId=authorization_code.member_id,
            scopes=authorization_code.scopes,
        )
        access_token = AccessToken(access_token_payload)
        return dict(
            accessToken=access_token.dump(),
            memberId=authorization_code.member_id
        )

