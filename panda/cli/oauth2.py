import sys

from restfulpy.orm import DBSession
from restfulpy.cli import Launcher, RequireSubCommand

from ..models import Member, Application, ApplicationMember
from ..oauth import AuthorizationCode, AccessToken


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
            'application_id',
            help='Application Id'
        )
        parser.add_argument(
            '-s', '--scopes',
            nargs='+',
            help='List of oauth2 scopes'
        )
        return parser

    def launch(self):
        member = DBSession.query(Member)\
            .filter(Member.id == self.args.member_id)\
            .one_or_none()

        if member is None:
            print(f'Invalid member id: {self.args.member_id}', file=sys.stderr)
            return 1

        application = DBSession.query(Application)\
            .filter(Application.id == self.args.application_id)\
            .one_or_none()

        if application is None:
            print(f'Invalid application id: {self.args.application_id}', file=sys.stderr)
            return 1

        authorization_code_payload = dict(
            scopes=self.args.scopes,
            memberId=member.id,
            memberTitle=member.title,
            email=member.email,
            applicationId=application.id,
            applicationTitle=application.title,
            location='/'
        )
        authorization_code = AuthorizationCode(authorization_code_payload)

        application = DBSession.query(Application) \
            .filter(Application.id == application.id) \
            .one_or_none()

        if not application:
            raise HTTPUnRecognizedApplication()

        application_member = DBSession.query(ApplicationMember) \
            .filter(
                ApplicationMember.application_id == application.id,
                ApplicationMember.member_id == authorization_code.member_id
            ) \
            .one_or_none()

        if not application_member:
            application_member = ApplicationMember(
                application_id=application.id,
                member_id=authorization_code.member_id
            )
            DBSession.add(application_member)

        access_token_payload = dict(
            applicationId=application.id,
            memberId=authorization_code.member_id,
            scopes=authorization_code.scopes,
        )
        access_token = AccessToken(access_token_payload)
        print(access_token.dump().decode())


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



