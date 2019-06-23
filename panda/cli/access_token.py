import sys

from easycli import SubCommand, Argument
from restfulpy.orm import DBSession

from ..models import Member, Application, ApplicationMember
from ..oauth import AccessToken


class AccessTokenCreateSumSubCommand(SubCommand): # pragma: no cover
    __help__ = 'Creates an jwt token.'
    __command__ = 'create'
    __arguments__ = [
        Argument(
            'member_id',
            type=int,
            help='Member id',
        ),
        Argument(
            'application_id',
            help='Application Id',
        ),
        Argument(
            '-s',
            '--scopes',
            nargs='+',
            help='List of oauth2 scopes',
        ),
    ]

    def __call__(self, args):
        member = DBSession.query(Member)\
            .filter(Member.id == args.member_id)\
            .one_or_none()

        if member is None:
            print(f'Invalid member id: {args.member_id}', file=sys.stderr)
            return 1

        application = DBSession.query(Application)\
            .filter(Application.id == args.application_id)\
            .one_or_none()

        if application is None:
            print(
                f'Invalid application id: {args.application_id}',
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
            scopes=args.scopes,
        )
        access_token = AccessToken(access_token_payload)
        print(access_token.dump().decode())


class AccessTokenSubCommand(SubCommand): # pragma: no cover
    __help__ = 'Access token related.'
    __command__ = 'access-token'
    __arguments__ = [
        AccessTokenCreateSumSubCommand,
    ]

