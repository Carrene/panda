import base64

from restfulpy.orm import DBSession

from .models import Application, Member


def insert(): # pragma: no cover
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
        owner=admin
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
    print('Application has been created.')
    print(
        f'  Title: {application.title}\n'
        f'  Secret: {secret}\n'
        f'  Redirect uri: {application.redirect_uri}\n'
        f'  Owner of application is admin\n'
    )

