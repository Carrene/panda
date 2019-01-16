import sys

from restfulpy.cli import Launcher, RequireSubCommand
from restfulpy.orm import DBSession

from ..models import Member, Application, ApplicationMember
from ..oauth import AccessToken


class AccessTokenCreateLauncher(Launcher):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'create',
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
            print(
                f'Invalid application id: {self.args.application_id}',
                file=sys.stderr
            )
            return 1

        application_member = DBSession.query(ApplicationMember) \
            .filter(
                ApplicationMember.application_id == application.id,
                ApplicationMember.member_id == member.id
            ) \
            .one_or_none()

        if not application_member:
            application_member = ApplicationMember(
                application_id=application.id,
                member_id=member.id,
            )
            DBSession.add(application_member)
            DBSession.commit()

        access_token_payload = dict(
            applicationId=application.id,
            memberId=member.id,
            scopes=self.args.scopes,
        )
        access_token = AccessToken(access_token_payload)
        print(access_token.dump().decode())


class AccessTokenLauncher(Launcher, RequireSubCommand):

    @classmethod
    def create_parser(cls, subparsers):
        parser = subparsers.add_parser(
            'access-token',
            help='Access token related.'
        )
        oauth2_subparsers = parser.add_subparsers(
            title='Access token',
            dest='access_token_command'
        )
        AccessTokenCreateLauncher.register(oauth2_subparsers)
        return parser

