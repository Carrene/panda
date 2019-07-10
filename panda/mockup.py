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

    member4 = Member(
        id=5,
        title='User_4',
        name='User4_name',
        email='user4@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member4)

    member5 = Member(
        id=6,
        title='User_5',
        name='User5_name',
        email='user5@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member5)


    member6 = Member(
        id=7,
        title='User_6',
        name='User6_name',
        email='user6@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member6)

    member7 = Member(
        id=8,
        title='User_7',
        name='User7_name',
        email='user7@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member7)

    member8 = Member(
        id=9,
        title='User_8',
        name='User8_name',
        email='user8@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member8)

    member9 = Member(
        id=10,
        title='User_9',
        name='User9_name',
        email='user9@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member9)
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
    print(
        f'  Title: {member4.title}\n'
        f'  Name: {member4.name}\n'
        f'  Email: {member4.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member4.role}\n'
        f'  Phone: {member4.phone}\n'
    )
    print(
        f'  Title: {member5.title}\n'
        f'  Name: {member5.name}\n'
        f'  Email: {member5.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member5.role}\n'
        f'  Phone: {member5.phone}\n'
    )
    print(
        f'  Title: {member6.title}\n'
        f'  Name: {member6.name}\n'
        f'  Email: {member6.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member6.role}\n'
        f'  Phone: {member6.phone}\n'
    )
    print(
        f'  Title: {member6.title}\n'
        f'  Name: {member6.name}\n'
        f'  Email: {member6.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member6.role}\n'
        f'  Phone: {member6.phone}\n'
    )
    print(
        f'  Title: {member7.title}\n'
        f'  Name: {member7.name}\n'
        f'  Email: {member7.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member7.role}\n'
        f'  Phone: {member7.phone}\n'
    )
    print(
        f'  Title: {member8.title}\n'
        f'  Name: {member8.name}\n'
        f'  Email: {member8.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member8.role}\n'
        f'  Phone: {member8.phone}\n'
    )
    print(
        f'  Title: {member9.title}\n'
        f'  Name: {member9.name}\n'
        f'  Email: {member9.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member9.role}\n'
        f'  Phone: {member9.phone}\n'
    )

