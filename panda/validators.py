from nanohttp import validate


email_validator = validate(
    email=dict(
        required=(True, '701 Invalid email format'),
        pattern=(
            '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
            '701 Invalid email format'
        )
    )
)

