from restfulpy.orm import Field, PaginationMixin, FilteringMixin, \
    OrderingMixin, BaseModel, ModifiedMixin, TimestampMixin, relationship, \
    DBSession
from sqlalchemy import Integer, Unicode, select, and_, FLOAT, or_, ARRAY, func
from sqlalchemy.orm import mapper

from . import Organization, OrganizationMember, Member


class AbstractOrganizationMemberView(PaginationMixin, OrderingMixin, \
                                     FilteringMixin, BaseModel):
    __abstract__ = True
    __table_args__ = {'autoload': True}

    id = Field('id', Integer, primary_key=True )

    @classmethod
    def create_mapped_class(cls):

        query = select([Organization]).select_from(Organization)
        owner_cte = select([
            Member.id,
            Member.title,
            OrganizationMember.organization_id,
        ]).select_from(Member.__table__.outerjoin(
            OrganizationMember,
            and_(
                OrganizationMember.member_id == Member.id,
                OrganizationMember.role == 'owner'
            )
        )).cte()

        member_cte = select([
            Member.id,
            Member.title,
            OrganizationMember.organization_id,
        ]).select_from(Member.__table__.outerjoin(
            OrganizationMember,
            and_(
                OrganizationMember.member_id == Member.id,
                OrganizationMember.role == 'member'
            )
        )).cte()

        query = select([
            Organization.id,
            func.array_agg(func.json_build_object(
                'id',
                owner_cte.c.id,
                'title',
                owner_cte.c.title,
            )).label('owners'),
            func.array_agg(func.json_build_object(
                'id',
                member_cte.c.id,
                'title',
                member_cte.c.title
            )).label('members'),
        ]).select_from(Organization.__table__.outerjoin(
            member_cte,
            member_cte.c.organization_id == Organization.id
        ).join(
            owner_cte,
            owner_cte.c.organization_id == Organization.id
        )).group_by(
            Organization.id
        )

        class OrganizationMemberView(cls):
            pass

        mapper(OrganizationMemberView, query.alias())
        return OrganizationMemberView

    def to_dict(self):
        import pudb; pudb.set_trace()  # XXX BREAKPOINT
        view = super().to_dict()
        view['members'] = [x for x in view['members'] if x['id'] != None]
        view['owners'] = [x for x in view['owners'] if x['id'] != None]
        return view

