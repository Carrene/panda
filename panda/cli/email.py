from easycli import SubCommand, Argument
from nanohttp import settings

from ..models import RegisterEmail
from ..tokens import RegistrationToken


class SendEmailSubCommand(SubCommand):  # pragma: no cover
    __help__ = 'Sends an email.'
    __command__ = 'send'
    __arguments__ = [
        Argument(
            '-e',
            '--email',
            required=True,
            help='Email to be claim',
        ),
    ]

    def __call__(self, args):
        token = RegistrationToken(dict(email=args.email))
        email = RegisterEmail(
                to=args.email,
                subject='Register your CAS account',
                body={
                    'registration_token': token.dump(),
                    'registration_callback_url':
                        settings.registration.callback_url
                }
        )
        email.to = args.email
        email.do_({})

