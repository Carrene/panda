from nanohttp import context, json, HTTPStatus
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
        organization = DBSession.query(Organization). \
            filter(Organization.name == context.form.get('name')) \
            .one_or_none()
        if organization is not None:
            raise HTTPStatus('622 Organization Name Is Already Taken')

        member = Member.current()
        organization = Organization(
            name=context.form.get('name'),
            members=[member],
        )
        DBSession.add(organization)
        return organization

