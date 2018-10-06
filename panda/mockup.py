import base64

from restfulpy.orm import DBSession

from .models import Application, Member


def insert(): # pragma: no cover
    member1 = Member(
        title='john',
        email='john@gmail.com',
        password='123abcABC',
        role='member'
    )
    DBSession.add(member1)

    member2 = Member(
        title='tom',
        email='tom@gmail.com',
        password='123abcABC',
        role='member'
    )
    DBSession.add(member2)

    member3 = Member(
        title='sarah',
        email='sarah@gmail.com',
        password='123abcABC',
        role='member'
    )
    DBSession.add(member3)
    DBSession.flush()

    admin = Member(
        title='admin',
        email='admin@gmail.com',
        password='123abcABC',
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
        f'  Password: 123abcABC\n'
        f'  Role: {admin.role}\n'
    )
    print('Members have been created.')
    print(
        f'  Title: {member1.title}\n'
        f'  Email: {member1.email}\n'
        f'  Password: 123abcABC\n'
        f'  Role: {member1.role}\n'
    )
    print(
        f'  Title: {member2.title}\n'
        f'  Email: {member2.email}\n'
        f'  Password: 123abcABC\n'
        f'  Role: {member1.role}\n'
    )
    print(
        f'  Title: {member3.title}\n'
        f'  Email: {member3.email}\n'
        f'  Password: 123abcABC\n'
        f'  Role: {member1.role}\n'
    )
    print('Application has been created.')
    print(
        f'  Title: {application.title}\n'
        f'  Secret: {secret}\n'
        f'  Redirect uri: {application.redirect_uri}\n'
        f'  Owner of application is john\n'
    )

