from nanohttp import settings
from restfulpy.cli import Launcher, RequireSubCommand
from restfulpy.orm import DBSession

from ..models import RegisterEmail, Application


class ApplicationListLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('list', help='List applications.')
        return parser

    def launch(self):
        for m in DBSession.query(Application):
            print(m)


class ApplicationLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'application',
            help="Manage applications"
        )
        _subparsers = parser.add_subparsers(
            title="Applications managements",
            dest="application_command"
        )
        ApplicationListLauncher.register(_subparsers)
        return parser

