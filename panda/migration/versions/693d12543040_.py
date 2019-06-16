"""empty message

Revision ID: 693d12543040
Revises: 0f0474fa0d16
Create Date: 2019-06-16 17:42:34.337790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from panda.models import Member


# revision identifiers, used by Alembic.
revision = '693d12543040'
down_revision = '0f0474fa0d16'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    members = session.query(Member).all()
    for member in members:
        if member.name is None:
            member.name = member.title

    session.commit()

    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'member',
        'name',
        existing_type=sa.VARCHAR(length=20),
        nullable=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('member', 'name',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    # ### end Alembic commands ###