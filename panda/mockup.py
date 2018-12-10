from restfulpy.orm import DBSession
from nanohttp.contexts import Context
from nanohttp import context

from .models import Member, Organization, OrganizationMember


def insert(): # pragma: no cover
    member1 = Member(
        title='User_1',
        email='user1@example.com',
        password='123456',
        role='member',
        phone='+989351234567',
    )
    DBSession.add(member1)

    member2 = Member(
        title='User_2',
        email='user2@example.com',
        password='123456',
        role='member',
        phone='+989121234567',
    )
    DBSession.add(member2)

    member3 = Member(
        title='User_3',
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
        f'  Email: {member1.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member1.role}\n'
        f'  Phone: {member1.phone}\n'
    )
    print(
        f'  Title: {member2.title}\n'
        f'  Email: {member2.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member2.role}\n'
        f'  Phone: {member2.phone}\n'
    )
    print(
        f'  Title: {member3.title}\n'
        f'  Email: {member3.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member3.role}\n'
        f'  Phone: {member3.phone}\n'
    )

