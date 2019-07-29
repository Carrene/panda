
def get_title(member):
    return member.title


def get_email(member):
    return member.email


def get_first_name(member):
    return member.first_name


def get_last_name(member):
    return member.last_name


def get_avatar(member):
    return member.avatar


def get_phone(member):
    return member.phone


SCOPES = {
    'title': get_title,
    'email': get_email,
    'firstName': get_first_name,
    'lastName': get_last_name,
    'avatar': get_avatar,
    'phone': get_phone,
}

