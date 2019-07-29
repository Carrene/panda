"""empty message

Revision ID: 14c6dfb41269
Revises: 693d12543040
Create Date: 2019-07-29 14:57:50.798162

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from panda.models import Member


# revision identifiers, used by Alembic.
revision = '14c6dfb41269'
down_revision = '693d12543040'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    op.execute('alter table member rename name to first_name;')
    op.add_column(
        'member',
        sa.Column('last_name', sa.Unicode(length=20), nullable=True)
    )
    for member in session.query(Member):
        member.last_name = ''

    session.commit()

    op.execute('ALTER TABLE member ALTER last_name SET NOT NULL;')

def downgrade():
    op.execute('alter table member rename first_name to name;')
    op.drop_column('member', 'last_name')

