from nanohttp import context, json, HTTPStatus
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession

from ..models import Member, Organization
from ..validators import organization_title_validator


class OrganizationController(ModelRestController):
    __model__ = Organization

    @authorize
    @json(prevent_empty_form=True)
    @organization_title_validator
    @Organization.expose
    @commit
    def create(self):
        organization = DBSession.query(Organization) \
            .filter(Organization.title== context.form.get('title')) \
            .one_or_none()
        if organization is not None:
            raise HTTPStatus('622 Organization Title Is Already Taken')

        member = Member.current()
        organization = Organization(
            title=context.form.get('title'),
            members=[member],
        )
        DBSession.add(organization)
        return organization

