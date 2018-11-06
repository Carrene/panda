from nanohttp import context, json, HTTPStatus, validate, HTTPForbidden
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession

from ..models import Member, Organization
from ..validators import organization_validator


class OrganizationController(ModelRestController):
    __model__ = Organization

    @authorize
    @json(prevent_empty_form=True)
    @organization_validator
    @Organization.expose
    @commit
    def create(self):
        current_member = Member.current()
        organization = Organization(
            name = context.form.get('name')
        )
        return dict(organization)

