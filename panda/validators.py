import re

from nanohttp import validate, HTTPStatus


USER_EMAIL_PATTERN = \
    re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
USER_TITLE_PATTERN = re.compile('^[a-zA-Z][\w]{5,16}$')

# Password be to have numbers, uppercase, and lowercase
USER_PASSWORD_PATTERN = re.compile('(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+')


def application_title_value_validation(title, container, field):
    if title is None:
        return title

    if not title or title.isspace():
        raise HTTPStatus('712 Title Is Blank')

    return title


def application_redirect_uri_value_validation(redirectUri, container, field):
    if redirectUri is None:
        return redirectUri

    if not redirectUri or redirectUri.isspace():
        raise HTTPStatus('706 Redirect URI Is Blank')

    return redirectUri


email_validator = validate(
    email=dict(
        required='701 Invalid Email Format',
        pattern=(USER_EMAIL_PATTERN, '701 Invalid Email Format')
    )
)


title_validator = validate(
    title=dict(
        required='705 Invalid Title Format',
        pattern=(USER_TITLE_PATTERN, '705 Invalid Title Format')
    )
)


password_validator = validate(
    password=dict(
        required='702 Invalid Password Length',
        min_length=(6,'702 Invalid Password Length'),
        max_length=(20,'702 Invalid Password Length'),
        pattern=(USER_PASSWORD_PATTERN, '703 Password Not Complex Enough')
    )
)


new_password_validator = validate(
    newPassword=dict(
        required='702 Invalid Password Length',
        min_length=(6,'702 Invalid Password Length'),
        max_length=(20,'702 Invalid Password Length'),
        pattern=(USER_PASSWORD_PATTERN, '703 Password Not Complex Enough')
    )
)


application_validator = validate(
    title=dict(
        callback=application_title_value_validation
    ),
    redirectUri=dict(
        callback=application_redirect_uri_value_validation
    )
)

