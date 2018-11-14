import re

from nanohttp import validate, HTTPStatus, context


USER_EMAIL_PATTERN = \
    re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
USER_TITLE_PATTERN = re.compile(r'^[a-zA-Z][\w]{5,19}$')

# Password be to have numbers, uppercase, and lowercase
USER_PASSWORD_PATTERN = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+')
PHONE_PATTERN = re.compile(r'^[+]{0,1}[\d+]{7,15}$')
NAME_PATTERN = re.compile(r'^[a-zA-Z]{1}[a-z-A-Z ,.\'-]{2,19}$')
ORGANIZATION_TITLE_PATTERN = \
    re.compile(r'^([0-9a-zA-Z]+-?[0-9a-zA-Z]*)*[\da-zA-Z]$')
URL_PATTERN = re.compile(
    r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www.)+[a-z0-9]' \
    r'+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
)
DOMAIN_PATTERN = re.compile(
    r'^[^www.][a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?$'
)


def application_title_value_validation(title, container, field):
    if 'title' in context.form and (not title or title.isspace()):
        raise HTTPStatus('712 Title Is Blank')

    return title


def application_redirect_uri_value_validation(redirectUri, container, field):
    if 'redirectUri' in context.form and \
            (not redirectUri or redirectUri.isspace()):
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
        required='718 Title Not In Form',
        pattern=(USER_TITLE_PATTERN, '705 Invalid Title Format')
    )
)


password_validator = validate(
    password=dict(
        required='728 Password Not In Form',
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


phone_number_validator = validate(
    phoneNumber=dict(
        required='713 Invalid Phone Number',
        pattern=(PHONE_PATTERN, '713 Invalid Phone Number')
    )
)


member_validator = validate(
    name=dict(
        pattern=(NAME_PATTERN, '716 Invalid Name Format')
    ),
)


organization_create_validator = validate(
    title=dict(
        required='718 Title Not In Form',
        min_length=(1,'719 At Least 1 Character Is Needed For Title'),
        max_length=(40,'720 At Most 40 Characters Are Valid For Title'),
        pattern=(ORGANIZATION_TITLE_PATTERN, '705 Invalid Title Format'),
    ),
)


organization_title_validator = validate(
    title=dict(
        min_length=(1,'719 At Least 1 Character Is Needed For Title'),
        max_length=(40,'720 At Most 40 Characters Are Valid For Title'),
        pattern=(ORGANIZATION_TITLE_PATTERN, '705 Invalid Title Format'),
    ),
)


organization_domain_validator = validate(
    domain=dict(
        pattern=(DOMAIN_PATTERN, '726 Invalid Domain Format'),
    ),
)


organization_url_validator = validate(
    url=dict(
        pattern=(URL_PATTERN, '725 Invalid URL Format'),
    ),
)

