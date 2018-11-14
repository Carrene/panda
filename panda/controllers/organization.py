from nanohttp import context, json, HTTPStatus, HTTPNotFound
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from sqlalchemy_media import store_manager

from ..models import Member, Organization, OrganizationMember
from ..validators import organization_create_validator, \
    organization_title_validator, organization_domain_validator, \
    organization_url_validator


class OrganizationController(ModelRestController):
    __model__ = Organization

    @authorize
    @json(prevent_empty_form=True)
    @organization_create_validator
    @Organization.expose
    @commit
    def create(self):
        organization = DBSession.query(Organization) \
            .filter(Organization.title == context.form.get('title')) \
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

    @authorize
    @store_manager(DBSession)
    @json(prevent_empty_form=True)
    @organization_title_validator
    @organization_url_validator
    @organization_domain_validator
    @Organization.expose
    @commit
    def update(self, id):
        try:
            id = int(id)
        except (ValueError, TypeError):
            raise HTTPNotFound()

        organization = DBSession.query(Organization).get(id)
        if organization is None:
            raise HTTPNotFound()

        organization_member = DBSession.query(OrganizationMember) \
            .filter(
                OrganizationMember.member_id == context.identity.reference_id,
                OrganizationMember.organization_id == id
            ) \
            .one_or_none()
        if organization_member is None:
            raise HTTPNotFound()

        if organization_member.role != 'owner':
            raise HTTPNotFound()

        title = context.form.get('title')
        if title is not None and organization.title != title:
            organ = DBSession.query(Organization) \
                .filter(Organization.title == title) \
                .one_or_none()
            if organ is not None:
                raise HTTPStatus('622 Organization Title Is Already Taken')

        organization.update_from_request()
        return organization

