from restfulpy.messaging.models import Email


class RegisterEmail(Email):
    __mapper_args__ = {
        'polymorphic_identity': 'register_email'
    }

    template_filename = 'register_email.mako'

