
def get_title(member):
    return member.title


def get_email(member):
    return member.email


SCOPES = {
    'title': get_title,
    'email': get_email
}

