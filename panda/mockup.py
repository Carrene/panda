import base64

from restfulpy.orm import DBSession

from .models import Client, Member


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
    client = Client(
        title='oauth',
        redirect_uri='http://example.com/oauth',
        secret=base64.decodebytes(bytes(secret, 'utf-8')),
        member_id=member1.id
    )
    DBSession.add(client)
    DBSession.commit()

    print('# Members has been created')
    print(
        f' Title: {member1.title}\n Email: {member1.email}\n '
        'Password: 123abcABC\n'
    )
    print(
        f' Title: {member2.title}\n Email: {member2.email}\n '
        'Password: 123abcABC\n'
    )
    print(
        f' Title: {member3.title}\n Email: {member3.email}\n '
        'Password: 123abcABC\n'
    )
    print('# Client has been created')
    print(
        f' Title: {client.title}\n Secret: {secret}\n '
        'Redirect uri: {client.redirect_uri}\n')

