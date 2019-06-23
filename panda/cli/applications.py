from easycli import SubCommand
from restfulpy.orm import DBSession

from ..models import Application


class ApplicationListSubSubCommand(SubCommand): # pragma: no cover
    __help__ = 'List applications.'
    __command__ = 'list'

    def __call__(self, args):
        for m in DBSession.query(Application):
            print(m)


class ApplicationSubCommand(SubCommand): # pragma: no cover
    __help__ = 'Manage applications'
    __command__ = 'application'
    __arguments__ = [
        ApplicationListSubSubCommand,
    ]

