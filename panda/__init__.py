import functools
from os.path import join, dirname

from nanohttp import settings
from restfulpy.application import Application
from sqlalchemy_media import StoreManager, FileSystemStore

from . import basedata
from .authentication import Authenticator
from .cli.email import EmailLauncher
from .controllers.root import Root


__version__ = '0.3.0nightly'


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
      callback_url: http://nightly.cas.carrene.com/signup

    messaging:
      default_messenger: restfulpy.messaging.SmtpProvider
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

    smtp:
      host: smtp.gmail.com
      username: cas@carrene.com
      password: <password>
      local_hostname: carrene.com

    sms:
      provider: panda.sms.ConsoleSmsProvider
      cm:
        sender: cas@Carrene
        refrence: Carrene
        token: <token>
        url: https://gw.cmtelecom.com/v1.0/message
      kavenegar:
        apiKey: <key>

    phone:
      activation_token:
        secret: !!binary dKcWy4fQTpgjjAhS6SbapQUvtxPhiO23GguaV9U1y7k=
        max_age: 360  # seconds
        algorithm: HS256
      activation_code:
        length: 6
        hash_algorithm: SHA-1
        time_interval: 59 # seconds
        challenge_limit: 40
        seed: !!python/bytes 8QYEd+yEh4fcZ5aAVqrlXBWuToeXTyOeHFun8OzOL48=
        window: 4
      jwt:
        max_age: 86400

    storage:
      file_system_dir: %(root_path)s/data/assets
      base_url: http://localhost:8080/assets
    '''

    def __init__(self, application_name='panda', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    def insert_basedata(self, *args):
        basedata.insert()

    def register_cli_launchers(self, subparsers):
        EmailLauncher.register(subparsers)

    @classmethod
    def initialize_orm(cls, engine=None):
        StoreManager.register(
            'fs',
            functools.partial(
                FileSystemStore,
                settings.storage.file_system_dir,
                base_url=settings.storage.base_url,
            ),
            default=True
        )
        super().initialize_orm(cls, engine)


panda = Panda()

