from easycli import SubCommand
from restfulpy.orm import DBSession

from ..models import Application


class ApplicationListSubSubCommand(SubCommand):
    __help__ = 'List applications.'
    __command__ = 'list'

    def __call__(self, args):
        for m in DBSession.query(Application):
            print(m)


class ApplicationSubCommand(SubCommand):
    __help__ = 'Manage applications'
    __command__ = 'application'
    __arguments__ = [
        ApplicationListSubSubCommand,
    ]

