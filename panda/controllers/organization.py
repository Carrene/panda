from nanohttp import context, json, HTTPStatus, HTTPNotFound, HTTPForbidden, \
    settings
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from sqlalchemy import exists, and_
from sqlalchemy_media import store_manager

from ..models import Member, Organization, OrganizationMember, \
    JoinOrganizationEmail
from ..tokens import JoinOrganizationToken
from ..validators import organization_create_validator, \
    organization_title_validator, organization_domain_validator, \
    organization_url_validator, email_validator, organization_role_validator


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
            is_title_already_exist = DBSession \
                .query(exists().where(Organization.title == title)) \
                .scalar()
            if is_title_already_exist:
                raise HTTPStatus('622 Organization Title Is Already Taken')

        organization.update_from_request()
        return organization

    @authorize
    @store_manager(DBSession)
    @json(prevent_empty_form=True)
    @email_validator
    @organization_role_validator
    @Organization.expose
    @commit
    def invite(self, id):
        try:
            id = int(id)
        except (ValueError, TypeError):
            raise HTTPNotFound()

        organization = DBSession.query(Organization).get(id)
        if organization is None:
            raise HTTPNotFound()

        email = context.form.get('email')
        member = DBSession.query(Member) \
            .filter(Member.email == email) \
            .one_or_none()
        if member is None:
            raise HTTPNotFound()

        organization_member = DBSession.query(OrganizationMember). \
            filter(
                OrganizationMember.organization_id == id,
                OrganizationMember.member_id == context.identity.reference_id
            ) \
            .one_or_none()
        if organization_member is None or organization_member.role != 'owner':
            raise HTTPForbidden()

        is_already_join = DBSession.query(exists().where(and_(
            OrganizationMember.organization_id == id,
            OrganizationMember.member_id == member.id
        ))).scalar()
        if is_already_join:
            raise HTTPStatus('623 Already In This Organization')

        token = JoinOrganizationToken(dict(
            email=email,
            organization_id=id,
            member_id=member.id,
            owner_id=context.identity.reference_id,
            role=context.form.get('role'),
        ))
        DBSession.add(
            JoinOrganizationEmail(
                to=email,
                subject='Invite to organization',
                body={
                    'token': token.dump(),
                    'callback_url': settings.join_organization.callback_url
                }
            )
        )
        return organization

