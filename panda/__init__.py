from os.path import join, dirname

from restfulpy.application import Application

from .controllers.root import Root


__version__ = '0.1.0-dev'


class Panda(Application):

    builtin_configuration = """
    reset_password:
      secret: reset-password-secret
      max_age: 3600  # seconds
      url: http://nc.carrene.com/reset_password
      # url: http://localhost:8080/reset_password

    activation:
      secret: activation-secret
      max_age: 86400  # seconds
      url: http://nc.carrene.com/activate
      # url: http://localhost:8080/activate
      """

    def __init__(self):
        super().__init__(
            'panda',
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )


panda = Panda()

