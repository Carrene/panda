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
        first_name='User1_first_name',
        last_name='User1_last_name',
        email='user1@example.com',
        password='123456',
        role='member',
        phone='+989351234567',
    )
    DBSession.add(member1)

    member2 = Member(
        id=3,
        title='User_2',
        first_name='User2_first_name',
        last_name='User2_last_name',
        email='user2@example.com',
        password='123456',
        role='member',
        phone='+989121234567',
    )
    DBSession.add(member2)

    member3 = Member(
        id=4,
        title='User_3',
        first_name='User3_first_name',
        last_name='User3_last_name',
        email='user3@example.com',
        password='123456',
        role='member',
        phone='+989361234567',
    )
    DBSession.add(member3)

    member4 = Member(
        id=5,
        title='User_4',
        first_name='User4_first_name',
        last_name='User4_last_name',
        email='user4@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member4)

    member5 = Member(
        id=6,
        title='User_5',
        first_name='User5_first_name',
        last_name='User5_last_name',
        email='user5@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member5)

    member6 = Member(
        id=7,
        title='User_6',
        first_name='User6_first_name',
        last_name='User6_last_name',
        email='user6@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member6)

    member7 = Member(
        id=8,
        title='User_7',
        first_name='User7_first_name',
        last_name='User7_last_name',
        email='user7@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member7)

    member8 = Member(
        id=9,
        title='User_8',
        first_name='User8_first_name',
        last_name='User8_last_name',
        email='user8@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member8)

    member9 = Member(
        id=10,
        title='User_9',
        first_name='User9_first_name',
        last_name='User9_last_name',
        email='user9@example.com',
        password='123456',
        role='member',
    )
    DBSession.add(member9)
    DBSession.commit()

    print('Members have been created.')
    print(
        f'  Title: {member1.title}\n'
        f'  First Name: {member1.first_name}\n'
        f'  Last Name: {member1.last_name}\n'
        f'  Email: {member1.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member1.role}\n'
        f'  Phone: {member1.phone}\n'
    )
    print(
        f'  Title: {member2.title}\n'
        f'  First Name: {member1.first_name}\n'
        f'  Last Name: {member1.last_name}\n'
        f'  Email: {member2.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member2.role}\n'
        f'  Phone: {member2.phone}\n'
    )
    print(
        f'  Title: {member3.title}\n'
        f'  First Name: {member1.first_name}\n'
        f'  Last Name: {member1.last_name}\n'
        f'  Email: {member3.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member3.role}\n'
        f'  Phone: {member3.phone}\n'
    )
    print(
        f'  Title: {member4.title}\n'
        f'  First Name: {member4.first_name}\n'
        f'  Last Name: {member4.last_name}\n'
        f'  Email: {member4.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member4.role}\n'
        f'  Phone: {member4.phone}\n'
    )
    print(
        f'  Title: {member5.title}\n'
        f'  First Name: {member5.first_name}\n'
        f'  Last Name: {member5.last_name}\n'
        f'  Email: {member5.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member5.role}\n'
        f'  Phone: {member5.phone}\n'
    )
    print(
        f'  Title: {member6.title}\n'
        f'  First Name: {member6.first_name}\n'
        f'  Last Name: {member6.last_name}\n'
        f'  Email: {member6.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member6.role}\n'
        f'  Phone: {member6.phone}\n'
    )
    print(
        f'  Title: {member6.title}\n'
        f'  First Name: {member6.first_name}\n'
        f'  Last Name: {member6.last_name}\n'
        f'  Email: {member6.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member6.role}\n'
        f'  Phone: {member6.phone}\n'
    )
    print(
        f'  Title: {member7.title}\n'
        f'  First Name: {member7.first_name}\n'
        f'  Last Name: {member7.last_name}\n'
        f'  Email: {member7.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member7.role}\n'
        f'  Phone: {member7.phone}\n'
    )
    print(
        f'  Title: {member8.title}\n'
        f'  First Name: {member8.first_name}\n'
        f'  Last Name: {member8.last_name}\n'
        f'  Email: {member8.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member8.role}\n'
        f'  Phone: {member8.phone}\n'
    )
    print(
        f'  Title: {member9.title}\n'
        f'  First Name: {member9.first_name}\n'
        f'  Last Name: {member9.last_name}\n'
        f'  Email: {member9.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member9.role}\n'
        f'  Phone: {member9.phone}\n'
    )

