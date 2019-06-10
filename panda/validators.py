import re

from nanohttp import validate, HTTPStatus, context

from .models.organization import roles


USER_TITLE_PATTERN = re.compile(r'^[a-zA-Z][\w\ ]{5,19}$')
USER_PASSWORD_PATTERN = re.compile(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).+')
PHONE_PATTERN = re.compile(r'^[+]{0,1}[\d+]{7,15}$')
NAME_PATTERN = re.compile(r'^[a-zA-Z]{1}[a-z-A-Z ,.\'-]{2,19}$')
USER_EMAIL_PATTERN = re.compile(
    r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
)
ORGANIZATION_TITLE_PATTERN = re.compile(
    r'^([0-9a-zA-Z]+-?[0-9a-zA-Z]*)*[\da-zA-Z]$'
)
URL_PATTERN = re.compile(
    r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www.)+[a-z0-9]'
    r'+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\.*)?$'
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


def organization_value_of_role_validator(role, container, field):
    if context.form.get('role') not in roles:
        raise HTTPStatus('724 Invalid Role Value')

    return role


email_validator = validate(
    email=dict(
        required='722 Email Not In Form',
        pattern=(USER_EMAIL_PATTERN, '701 Invalid Email Format')
    )
)


title_validator = validate(
    title=dict(
        required='718 Title Not In Form',
        pattern=(USER_TITLE_PATTERN, '705 Invalid Title Format')
    )
)


member_register_validator = validate(
    ownershipToken=dict(
        required='727 Token Not In Form',
    ),
    title=dict(
        required='718 Title Not In Form',
        pattern=(USER_TITLE_PATTERN, '705 Invalid Title Format')
    ),
    name=dict(
        required='731 Name Not In Form',
        not_none='732 Name Is Null',
        max_length=(20, '733 At Most 20 Characters Are Valid For Name'),
        pattern=(NAME_PATTERN, '716 Invalid Name Format'),
    ),
    password=dict(
        required='728 Password Not In Form',
        min_length=(6,'702 Invalid Password Length'),
        max_length=(20,'702 Invalid Password Length'),
        pattern=(USER_PASSWORD_PATTERN, '703 Password Not Complex Enough')
    ),
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


member_update_validator = validate(
    name=dict(
        pattern=(NAME_PATTERN, '716 Invalid Name Format'),
        not_none='732 Name Is Null',
        max_length=(20, '733 At Most 20 Characters Are Valid For Name'),
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


organization_role_validator = validate(
    role=dict(
        required='723 Role Not In Form',
        callback=organization_value_of_role_validator,
    ),
)


token_validator = validate(
    token=dict(
        required='727 Token Not In Form',
    ),
)


reset_password_token_validator = validate(
    resetPasswordToken=dict(
        required='730 Reset Password Token Not In Form',
    ),
)

