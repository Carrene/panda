import base64

from restfulpy.orm import DBSession

from .models import Application, Member


def insert(): # pragma: no cover
    member1 = Member(
        title='john',
        email='john@gmail.com',
        password='123abcABC'
    )
    DBSession.add(member1)

    member2 = Member(
        title='tom',
        email='tom@gmail.com',
        password='123abcABC'
    )
    DBSession.add(member2)

    member3 = Member(
        title='sarah',
        email='sarah@gmail.com',
        password='123abcABC'
    )
    DBSession.add(member3)
    DBSession.flush()

    secret = 'A1dFVpz4w/qyym+HeXKWYmm6Ocj4X5ZNv1JQ7kgHBEk='
    application = Application(
        title='oauth',
        redirect_uri='http://example.com/oauth',
        secret=base64.decodebytes(bytes(secret, 'utf-8')),
        member_id=member1.id
    )
    DBSession.add(application)
    DBSession.commit()

    print('Members has been created.')
    print(
        f'  Title: {member1.title}\n'
        f'  Email: {member1.email}\n'
        f'  Password: 123abcABC\n'
    )
    print(
        f'  Title: {member2.title}\n'
        f'  Email: {member2.email}\n'
        f'  Password: 123abcABC\n'
    )
    print(
        f'  Title: {member3.title}\n'
        f'  Email: {member3.email}\n'
        f'  Password: 123abcABC\n'
    )
    print('Application has been created.')
    print(
        f'  Title: {application.title}\n'
        f'  Secret: {secret}\n'
        f'  Redirect uri: {application.redirect_uri}\n'
        f'  Related to member with id: {application.member_id}\n'
    )

