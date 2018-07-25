import re

from nanohttp import validate


USER_TITLE_PATTERN = re.compile('^[a-zA-Z][\w]{5,16}$')
USER_EMAIL_PATTERN =\
    re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')


email_validator = validate(
    email=dict(
        required=(True, '701 Invalid email format'),
        pattern=(USER_EMAIL_PATTERN, '701 Invalid email format')
    )
)


title_validator = validate(
    title=dict(
        required=(True, '705 Invalid title format'),
        pattern=(USER_TITLE_PATTERN, '705 Invalid title format')
    )
)

