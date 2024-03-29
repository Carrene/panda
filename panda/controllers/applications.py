import hashlib

from nanohttp import json, context, HTTPNotFound, int_or_notfound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import DBSession, commit
from sqlalchemy_media import store_manager

from .. import cryptohelpers
from ..exceptions import HTTPInvalidTitleFormat, HTTPBlankRedirectURI
from ..models import Application, ApplicationMember
from ..validators import application_validator


class ApplicationController(ModelRestController):
    __model__ = Application

    @json(prevent_empty_form=True)
    @authorize
    @Application.expose
    @commit
    def define(self):
        title = context.form.get('title')
        redirect_uri = context.form.get('redirectUri')

        if not title or title.isspace():
            raise HTTPInvalidTitleFormat()

        if not redirect_uri or redirect_uri.isspace():
            raise HTTPBlankRedirectURI()

        application = Application(
            title=title,
            redirect_uri=redirect_uri,
            owner_id=context.identity.reference_id
        )
        application.secret = hashlib.pbkdf2_hmac(
            'sha256',
            str(context.identity.id).encode(),
            cryptohelpers.random(32),
            100000,
            dklen=32
        )
        DBSession.add(application)
        return application

    @authorize
    @json
    @Application.expose
    @commit
    def get(self, id):
        id = int_or_notfound(id)

        application = DBSession.query(Application) \
            .filter(
                Application.id == id,
                Application.owner_id == context.identity.reference_id
            ) \
            .one_or_none()

        if application is None:
            raise HTTPNotFound()

        return application

    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    def list(self):
        return DBSession.query(Application)

    @authorize
    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    @commit
    def logout(self, id):
        id = int_or_notfound(id)

        application = DBSession.query(Application).get(id)
        if application is None:
            raise HTTPNotFound()

        application_member = DBSession.query(ApplicationMember) \
            .filter(
                ApplicationMember.application_id == id,
                ApplicationMember.member_id == context.identity.reference_id
            ) \
            .one_or_none()

        if application_member is None:
            raise HTTPNotFound()

        DBSession.delete(application_member)
        return application

    @authorize
    @store_manager(DBSession)
    @json(
        form_whitelist=(
            ['title', 'redirectUri', 'icon'],
            '717 Invalid field, only the title, redirectUri and icon ' \
            'parameters are accepted'
        ),
        prevent_empty_form=True
    )
    @application_validator
    @Application.expose
    @commit
    def update(self, id):
        id = int_or_notfound(id)

        application = DBSession.query(Application).get(id)
        if application is None:
            raise HTTPNotFound()

        if application.owner_id != context.identity.reference_id:
            raise HTTPNotFound()

        application.update_from_request()
        return application

    @authorize
    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    @commit
    def revoke(self, id):
        id = int_or_notfound(id)

        application = DBSession.query(Application).get(id)
        if application is None \
                or application.owner_id != context.identity.reference_id:
            raise HTTPNotFound()

        application.members.clear()
        return application

    @authorize
    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    @commit
    def delete(self, id):
        id = int_or_notfound(id)

        application = DBSession.query(Application).get(id)
        if application is None or \
                application.owner_id != context.identity.reference_id:
            raise HTTPNotFound()

        DBSession.delete(application)
        return application


class MyApplicationController(ModelRestController):
    __model__ = Application

    @authorize
    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    def list(self):
        return DBSession.query(Application) \
            .filter(Application.owner_id == context.identity.reference_id)


class AuthorizedApplicationController(ModelRestController):
    __model__ = Application

    @authorize
    @json(prevent_form='707 Form Not Allowed')
    @Application.expose
    def list(self):
        application = DBSession.query(Application) \
            .filter(
                ApplicationMember.member_id == context.identity.reference_id
            )
        return application

