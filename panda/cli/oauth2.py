from restfulpy.orm import DBSession
from restfulpy.cli import Launcher, RequireSubCommand

from ..models import Member
from ..oauth import AuthorizationCode


class OAuth2CreateTokenLauncher(Launcher):
    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'create-token',
            help='Creates an jwt token.'
        )
        parser.add_argument(
            'member_id',
            type=int,
            help='Member id'
        )
        parser.add_argument(
            '-s', '--scopes',
            nargs='+',
            help='List of oauth2 scopes'
        )
        parser.add_argument(
            '-i', '--application-id',
            help='Application Id'
        )
        parser.add_argument(
            '-t', '--application-title',
            help='Application Id'
        )
        return parser

    def launch(self):
        member = DBSession.query(Member)\
            .filter(Member.id == self.args.member_id)\
            .one_or_none()

        if member is None:
            print("Invalid member id: {self.args.member_is}", file=sys.stderr)

        authorization_code_payload = dict(
            scopes=self.args.scopes,
            memberId=member.id,
            memberTitle=member.title,
            email=member.email,
            applicationId=self.args.application_id,
            applicationTitle=self.args.application_title,
            location='/'
        )
        authorization_code = AuthorizationCode(authorization_code_payload)
        print(authorization_code.dump().decode())


class OAuth2Launcher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser('oauth2', help="OAUTH2 related.")
        oauth2_subparsers = parser.add_subparsers(
            title="OAUTH2",
            dest="oauth2_command"
        )
        OAuth2CreateTokenLauncher.register(oauth2_subparsers)
        return parser



