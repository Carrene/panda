import base64

from restfulpy.orm import DBSession

from .models import Application, Member


def insert(): # pragma: no cover
    member1 = Member(
        title='User 1',
        email='user1@example.com',
        password='123456',
        role='member'
    )
    DBSession.add(member1)

    member2 = Member(
        title='User 2',
        email='user2@example.com',
        password='123456',
        role='member'
    )
    DBSession.add(member2)

    member3 = Member(
        title='User 3',
        email='user3@example.com',
        password='123456',
        role='member'
    )
    DBSession.add(member3)
    DBSession.flush()

    admin = Member(
        title='admin',
        email='admin@example.com',
        password='123456',
        role='admin'
    )
    DBSession.add(admin)
    DBSession.flush()

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
    )
    print(
        f'  Title: {member2.title}\n'
        f'  Email: {member2.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member2.role}\n'
    )
    print(
        f'  Title: {member3.title}\n'
        f'  Email: {member3.email}\n'
        f'  Password: 123456\n'
        f'  Role: {member3.role}\n'
    )
    print('Application has been created.')
    print(
        f'  Title: {application.title}\n'
        f'  Secret: {secret}\n'
        f'  Redirect uri: {application.redirect_uri}\n'
        f'  Owner of application is User 1\n'
    )

