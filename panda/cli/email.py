from nanohttp import settings
from restfulpy.cli import Launcher, RequireSubCommand

from ..models import RegisterEmail
from ..tokens import RegisterationToken


class SendEmailLauncher(Launcher):  # pragma: no cover

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('send', help='Sends an email.')
        parser.add_argument(
            '-e',
            '--email',
            required=True,
            help='Email to be claim'
        )
        return parser

    def launch(self):
        token = RegisterationToken(dict(email=self.args.email))
        email = RegisterEmail(
                to=self.args.email,
                subject='Register your CAS account',
                body={
                    'registeration_token': token.dump(),
                    'registeration_callback_url':
                    settings.registeration.callback_url
                }
        )
        email.to = self.args.email
        email.do_({})


class EmailLauncher(Launcher, RequireSubCommand):  # pragma: no cover

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('email', help="Manage emails")
        user_subparsers = parser.add_subparsers(
            title="Email managements",
            dest="email_command"
        )
        SendEmailLauncher.register(user_subparsers)
        return parser

