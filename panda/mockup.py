import os
import base64

from restfulpy.orm import DBSession

from .models import Client, Member


def insert(): # pragma: no cover
    member1 = Member(
        title='john',
        email='john@gmail.com',
        password='123abcABC'
    )

    member2 = Member(
        title='tom',
        email='tom@gmail.com',
        password='123abcABC'
    )

    member3 = Member(
        title='sarah',
        email='sarah@gmail.com',
        password='123abcABC'
    )

    DBSession.add_all([member1, member2, member3])
    DBSession.flush()

    client = Client(
        title='oauth',
        redirect_uri='http://example.com/oauth',
        secret=base64.decodebytes(
            bytes('A1dFVpz4w/qyym+HeXKWYmm6Ocj4X5ZNv1JQ7kgHBEk=\n', 'utf-8')
        ),
        member_id=member1.id
    )

    secret = base64.encodebytes(client.secret)
    DBSession.add(client)
    DBSession.commit()

    print(member1.to_dict())

    print(f'member1: title:{member1.title} email:{member1.email} password:123abcABC')
    print(f'member2: title:{member2.title} email:{member2.email} password:123abcABC')
    print(f'member3: title:{member3.title} email:{member3.email} password:123abcABC')
    print(f'client: id:{client.id} title:{client.title} rediect_uri:{client.redirect_uri} member id:{client.member_id} secret:{secret}')

