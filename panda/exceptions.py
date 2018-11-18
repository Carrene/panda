from nanohttp import HTTPKnownStatus


class HTTPTokenExpired(HTTPKnownStatus):
    status = '609 Token Expired'


class HTTPMalformedToken(HTTPKnownStatus):
    status = '611 Malformed Token'


class HTTPBlankTitle(HTTPKnownStatus):
    status = '712 Title Is Blank'


class HTTPInvalidTitleFormat(HTTPKnownStatus):
    status = '705 Invalid Title Format'


class HTTPBlankRedirectURI(HTTPKnownStatus):
    status = '706 Redirect URI Is Blank'


class HTTPInvalidRoleValue(HTTPKnownStatus):
    status = 'Invalid Role Value'


class HTTPInvalidEmailFormat(HTTPKnownStatus):
    status = '701 Invalid Email Format'


class HTTPTitleNotInForm(HTTPKnownStatus):
    status = '718 Title Not In Form'


class HTTPPasswordNotInForm(HTTPKnownStatus):
    status =  '728 Password Not In Form'


class HTTPInvalidPasswordLength(HTTPKnownStatus):
    status = '702 Invalid Password Length'


class HTTPPasswordNotComplexEnough(HTTPKnownStatus):
    status = '703 Password Not Complex Enough'


class HTTPInvalidPhoneNumber(HTTPKnownStatus):
    status = '713 Invalid Phone Number'


class HTTPInvalidNameFormat(HTTPKnownStatus):
    status = '716 Invalid Name Format'


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






