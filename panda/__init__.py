from os.path import join, dirname

from restfulpy.application import Application

from . import mockup
from .authentication import Authenticator
from .controllers.root import Root


__version__ = '0.1.0-dev'


class Panda(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/panda_dev
      test_url: postgresql://postgres:postgres@localhost/panda_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    reset_password:
      secret: !!binary xxSN/uarj5SpcEphAHhmsab8Ql2Og/2IcieNfQ3PysI=
      max_age: 3600  # seconds
      algorithm: HS256
      callback_url: http://nc.carrene.com/reset_password
      # url: http://localhost:8080/reset_password

    registeration:
      secret: !!binary xxSN/uarj5SpcEphAHhmsab8Ql2Og/2IcieNfQ3PysI=
      max_age: 86400  # seconds
      algorithm: HS256
      callback_url: http://cas.carrene.com/register

    messaging:
      default_messenger: restfulpy.messaging.ConsoleMessenger
      template_dirs:
        - %(root_path)s/panda/email_templates

    authorization_code:
      secret: !!binary T8xNMJCFl4xgBSW3NaDv6/D+48ssBWZTQbqqDlnl0gU=
      max_age: 86400  # seconds
      algorithm: HS256

    access_token:
      secret: !!binary dKcWy4fQTpgjjAhS6SbapQUvtxPhiO23GguaV9U1y7k=
      max_age: 2592000  # seconds
      algorithm: HS256
    '''

    def __init__(self, application_name='panda', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    def insert_mockup(self):
        mockup.insert()


panda = Panda()

