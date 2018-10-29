import base64

from restfulpy.orm import DBSession

from .models import Application, Member


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

    admin = Member(
        title='admin',
        email='admin@example.com',
        password='123456',
        role='admin'
    )
    DBSession.add(admin)

    secret = 'A1dFVpz4w/qyym+HeXKWYmm6Ocj4X5ZNv1JQ7kgHBEk='
    application = Application(
        title='oauth',
        redirect_uri='http://example.com/oauth',
        secret=base64.decodebytes(bytes(secret, 'utf-8')),
        owner=member1
    )
    DBSession.add(application)
    DBSession.commit()

    print('Admin has been created.')
    print(
        f'  Title: {admin.title}\n'
        f'  Email: {admin.email}\n'
        f'  Password: 123456\n'
        f'  Role: {admin.role}\n'
    )
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
    print('Application has been created.')
    print(
        f'  Title: {application.title}\n'
        f'  Secret: {secret}\n'
        f'  Redirect uri: {application.redirect_uri}\n'
        f'  Owner of application is User 1\n'
    )

