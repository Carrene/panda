from restfulpy.orm import Field, PaginationMixin, FilteringMixin, \
    OrderingMixin, BaseModel, ModifiedMixin, TimestampMixin, relationship, \
    DBSession
from sqlalchemy import Integer, Unicode, select, and_, FLOAT, or_, ARRAY, func
from sqlalchemy.orm import mapper

from . import Organization, OrganizationMember, Member


class AbstractMamad(PaginationMixin, OrderingMixin, \
                                 FilteringMixin, ModifiedMixin, \
                                 TimestampMixin, BaseModel):
    __abstract__ = True
    __table_args__ = {'autoload': True}

    id = Field('id', Integer, primary_key=True )

    @classmethod
    def create_mapped_class(cls):


        query = select([
            Organization.id,
            OrganizationMember.role,
            func.array_agg(OrganizationMember.member_id).label('member_id'),
            func.array_agg(OrganizationMember.member_id).label('owner_id')
        ]).select_from(
            OrganizationMember.__table__.join(
                Organization,
                OrganizationMember.organization_id == Organization.id
            )
        ) \
            .group_by(
                Organization.id,
                OrganizationMember.role,
            )
        import pudb; pudb.set_trace()  # XXX BREAKPOINT


#        amdmins_cte = select([Member.id, Member.title]).select_from(Member.__table__.join(OrganizationMember, and_(Member.id == OrganizationMember.member_id, OrganizationMember.role == 'owner'))).cte()
#
#        members_agg = func.array_agg(
#            OrganizationMember.member_id,
#            label='member'
#        ).filter(OrganizationMember.role == 'member')
#
#        members_agg = DBSession.query(Member) \
#            .join(OrganizationMember, OrganizationMember.member_id == Member.id) \
#            .join(Organization, Organization.id == OrganizationMember.organization_id) \
#            .filter(OrganizationMember.role == 'members') \
#            .subquery()
#
#        owners_agg = DBSession.query(Member) \
#            .join(OrganizationMember, OrganizationMember.member_id == Member.id) \
#            .join(Organization, Organization.id == OrganizationMember.organization_id) \
#            .filter(OrganizationMember.role == 'owner') \
#            .subquery()
#
##        query = select([Organization.id, func.array_agg(OrganizationMember.role)]).select_from(Organization.__table__).group_by(OrganizationMember.organization_id, Organization.id)
#        query = select([
#            Organization.id,
#            members_agg,
#            owners_agg
#        ]) \
#            .select_from(
#                Organization.__table__.join(
#                    OrganizationMember,
#                    Organization.id == OrganizationMember.organization_id)
#            ).group_by(Organization.id)


        class Mamad(cls):
           pass

        mapper(Mamad, query.alias())
        return Mamad, query

