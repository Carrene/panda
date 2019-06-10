from restfulpy.orm import DBSession
from nanohttp.contexts import Context
from nanohttp import context

from .models import Member, Organization, OrganizationMember


def insert(): # pragma: no cover
    # These mockup datas are shared between panda and dolphin.
    # The GOD id is 1.

    member1 = Member(
        id=2,
        title='User_1',
        name='User1_name',
        email='user1@example.com',
        password='123456',
        role='member',
        phone='+989351234567',
    )
    DBSession.add(member1)

    member2 = Member(
        id=3,
        title='User_2',
        name='User2_name',
        email='user2@example.com',
        password='123456',
        role='member',
        phone='+989121234567',
    )
    DBSession.add(member2)

    member3 = Member(
        id=4,
        title='User_3',
        name='User3_name',
        email='user3@example.com',
        password='123456',
        role='member',
        phone='+989361234567',
    )
    DBSession.add(member3)
    DBSession.commit()

    print('Members have been created.')
    print(
        f'  Title: {member1.title}\n'
        f'  Name: {member1.name}\n'
        f'  Email: {member1.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member1.role}\n'
        f'  Phone: {member1.phone}\n'
    )
    print(
        f'  Title: {member2.title}\n'
        f'  Name: {member1.name}\n'
        f'  Email: {member2.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member2.role}\n'
        f'  Phone: {member2.phone}\n'
    )
    print(
        f'  Title: {member3.title}\n'
        f'  Name: {member1.name}\n'
        f'  Email: {member3.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member3.role}\n'
        f'  Phone: {member3.phone}\n'
    )

