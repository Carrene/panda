from nanohttp import context, json, HTTPNotFound, HTTPForbidden, settings
from restfulpy.authorization import authorize
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from sqlalchemy import exists, and_
from sqlalchemy_media import store_manager

from ..exceptions import HTTPOrganizationTitleAlreadyTaken, \
    HTTPAlreadyInThisOrganization
from ..models import Member, Organization, OrganizationMember, \
   OrganizationInvitationEmail, AbstractOrganizationMember
from ..tokens import OrganizationInvitationToken
from ..validators import token_validator, organization_create_validator, \
    organization_title_validator, organization_domain_validator, \
    organization_url_validator, email_validator, organization_role_validator


OrganizationMember = AbstractOrganizationMember.create_mapped_class()


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
            raise HTTPOrganizationTitleAlreadyTaken()

        member = Member.current()
        organization = Organization(
            title=context.form.get('title'),
        )
        DBSession.add(organization)
        DBSession.flush()

        organization_member = OrganizationMember(
            organization_id=organization.id,
            member_id=member.id,
            role='owner',
        )
        DBSession.add(organization_member)
        return organization

    @authorize
    @store_manager(DBSession)
    @json(
        form_whitelist=(
            ['title', 'url', 'domain', 'icon'],
            '717 Invalid field, only the title, url, domain and icon ' \
            'parameters are accepted'
        ),
        prevent_empty_form=True,
    )
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
                raise HTTPOrganizationTitleAlreadyTaken()

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

        organization_member = DBSession.query(OrganizationMember) \
            .filter(
                OrganizationMember.organization_id == id,
                OrganizationMember.member_id == context.identity.reference_id
            ) \
            .one_or_none()
        if organization_member is None or organization_member.role != 'owner':
            raise HTTPForbidden()

        is_member_in_organization = DBSession.query(exists().where(and_(
            OrganizationMember.organization_id == id,
            OrganizationMember.member_id == member.id
        ))).scalar()
        if is_member_in_organization:
            raise HTTPAlreadyInThisOrganization()

        token = OrganizationInvitationToken(dict(
            email=email,
            organizationId=id,
            memberId=member.id,
            ownerId=context.identity.reference_id,
            role=context.form.get('role'),
        ))
        DBSession.add(
            OrganizationInvitationEmail(
                to=email,
                subject='Invite to organization',
                body={
                    'token': token.dump(),
                    'callback_url':
                        settings.organization_invitation.callback_url
                }
            )
        )
        return organization

    @authorize
    @store_manager(DBSession)
    @json(prevent_empty_form=True)
    @token_validator
    @commit
    def join(self):
        token = OrganizationInvitationToken.load(context.form.get('token'))
        organization = DBSession.query(Organization).get(token.organization_id)
        if organization is None:
            raise HTTPNotFound()

        is_member_in_organization = DBSession.query(
            exists() \
            .where(
                OrganizationMember.organization_id == token.organization_id
            ) \
            .where(OrganizationMember.member_id == token.member_id)
        ).scalar()
        if is_member_in_organization:
            raise HTTPAlreadyInThisOrganization()

        organization_member = OrganizationMember(
            member_id=token.member_id,
            organization_id=organization.id,
            role=token.role,
        )
        DBSession.add(organization_member)
        return organization


class OrganizationMemberController(ModelRestController):

    @authorize
    @store_manager(DBSession)
    @json
    def list(self):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        query = DBSession.query(OrganizationMember).all()
        return query
