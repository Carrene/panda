import re

from nanohttp import validate


user_title_pattern = re.compile('^[a-zA-Z][\w]{5,16}$')


email_validator = validate(
    email=dict(
        required=(True, '701 Invalid email format'),
        pattern=(
            '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
            '701 Invalid email format'
        )
    )
)


title_validator = validate(
    title=dict(
        required=(True, '705 Invalid title format'),
        pattern=(user_title_pattern, '705 Invalid title format')
    )
)

