from nanohttp import HTTPKnownStatus


class HTTPTokenExpired(HTTPKnownStatus):
    status = '609 Token Expired'


class HTTPMalformedToken(HTTPKnownStatus):
    status = '611 Malformed Token'


class HTTPMalformedAccessToken(HTTPKnownStatus):
    status = '610 Malformed Access Token'


class HTTPMalformedAuthorizationCode(HTTPKnownStatus):
    status = '607 Malformed Authorization Code'


class HTTPInvalidTitleFormat(HTTPKnownStatus):
    status = '705 Invalid Title Format'


class HTTPBlankRedirectURI(HTTPKnownStatus):
    status = '706 Redirect URI Is Blank'


class HTTPInvalidRoleValue(HTTPKnownStatus):
    status = 'Invalid Role Value'


class HTTPPasswordNotComplexEnough(HTTPKnownStatus):
    status = '703 Password Not Complex Enough'


class HTTPInvalidPhoneNumber(HTTPKnownStatus):
    status = '713 Invalid Phone Number'


class HTTPEmailAddressAlreadyRegistered(HTTPKnownStatus):
    status = '601 Email Address Is Already Registered'


class HTTPTitleAlreadyRegistered(HTTPKnownStatus):
    status = '604 Title Is Already Registered'


class HTTPOrganizationTitleAlreadyTaken(HTTPKnownStatus):
    status = '622 Organization Title Is Already Taken'


class HTTPAlreadyInThisOrganization(HTTPKnownStatus):
    status = '623 Already In This Organization'


class HTTPInvalidCurrentPassword(HTTPKnownStatus):
    status = '602 Invalid Current Password'


class HTTPPhoneNumberAlreadyExists(HTTPKnownStatus):
    status = '616 Phone Number Already Exists'


class HTTPActivationCodeNotValid(HTTPKnownStatus):
    status = '617 Activation Code Is Not Valid'


class HTTPIncorrectEmailOrPassword(HTTPKnownStatus):
    status = '603 Incorrect Email Or Password'


class HTTPSecondPhoneNumber(HTTPKnownStatus):
    status = '615 Member Has The Phone Number'


class HTTPMalformedSecret(HTTPKnownStatus):
    status = '608 Malformed Secret'


class HTTPUnRecognizedApplication(HTTPKnownStatus):
    status = '605 We Don\'t Recognize This Application'


class HTTPInvalidScope(HTTPKnownStatus):
    status = '606 Invalid Scope'

