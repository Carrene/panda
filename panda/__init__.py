from os.path import join, dirname

from restfulpy.application import Application

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
      secret: reset-password-secret
      max_age: 3600  # seconds
      url: http://nc.carrene.com/reset_password
      # url: http://localhost:8080/reset_password

    registeration:
      secret: registeration-secret
      max_age: 86400  # seconds
      callback_url: http://cas.carrene.com/register

    messaging:
      default_sender: CAS
      template_dirs:
        - %(root_path)s/panda/email_templates

    '''

    def __init__(self):
        super().__init__(
            'panda',
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )


panda = Panda()

