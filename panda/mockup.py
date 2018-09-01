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

    print('\n***************  Members  ***************\n')
    print(member1.to_dict())
    print(member2.to_dict())
    print(member3.to_dict())
    print('\n*****************************************')

    print('***************  Clients  ***************\n')
    print(client.to_dict())
    print('\n*****************************************\n')
