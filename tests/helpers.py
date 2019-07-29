from os import path

from restfulpy.testing import ApplicableTestCase
from restfulpy.orm.metadata import FieldInfo

from panda import Panda, cryptohelpers
from panda.models import Application, Member, Organization


HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


code=FieldInfo(type_=str, required=True, not_none=True).to_json()
secret=FieldInfo(type_=str, required=True, not_none=True).to_json()
application_id=FieldInfo(type_=int, required=True, not_none=True).to_json()
scopes=FieldInfo(type_=str, required=True, not_none=True).to_json()
state=FieldInfo(type_=str, required=False, not_none=False).to_json()
redirect_uri=FieldInfo(type_=str, required=False, not_none=False).to_json()
email=FieldInfo(type_=str, required=True, not_none=True).to_json()
title=FieldInfo(type_=str, required=True, not_none=True).to_json()
password=FieldInfo(type_=str, required=True, not_none=True).to_json()
activation_code=FieldInfo(type_=str, required=True, not_none=True).to_json()
activation_token=FieldInfo(type_=str, required=True, not_none=True).to_json()
new_password=FieldInfo(type_=str, required=True, not_none=True).to_json()
password=FieldInfo(type_=str, required=True, not_none=True).to_json()
current_password=FieldInfo(type_=str, required=True, not_none=True).to_json()
phone_number=FieldInfo(type_=str, required=True, not_none=True).to_json()
role=FieldInfo(type_=str, required=True, not_none=True).to_json()
reset_password_token=FieldInfo(type_=str, required=True, not_none=True) \
    .to_json()


application_fields = Application.json_metadata()['fields']
reset_password_tokens_fields = dict(email=email)
email_fields = dict(email=email)
title_fields = dict(title=title)
tokens_fields = dict(email=email, password=password)
access_token_fields = dict(
    code=code,
    secret=secret,
    applicationId=application_id
)
authorization_code_fields = dict(
    applicationId=application_id,
    scopes=scopes,
    state=state,
    redirectUri=redirect_uri
)
phone_number_fields = dict(
    activationCode=activation_code,
    activationToken=activation_token,
    phoneNumber=phone_number
)
password_fields = dict(
    currentPassword=current_password,
    newPassword=new_password,
    password=password,
    resetPasswordToken=reset_password_token
)
organization_fields = Organization.json_metadata()['fields']
organization_fields.update(dict(
    email=email,
    role=role,
    title=title,
))


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')
    __metadata__ = {
        r'^/apiv1/applications.*': Application.json_metadata()['fields'],
        r'^/apiv1/members.*': Member.json_metadata()['fields'],
        r'^/apiv1/passwords.*': password_fields,
        r'^/apiv1/resetpasswordtokens.*': reset_password_tokens_fields,
        r'^/apiv1/accesstokens.*': access_token_fields,
        r'^/apiv1/authorizationcodes.*': authorization_code_fields,
        r'^/apiv1/emails.*': email_fields,
        r'^/apiv1/tokens.*': tokens_fields,
        r'^/apiv1/phonenumber.*': phone_number_fields,
        r'^/apiv1/availabilities/email.*': email_fields,
        r'^/apiv1/availabilities/nickname.*': title_fields,
        r'^/apiv1/organizations.*': organization_fields,
    }

    def login(self, email, password, url='/apiv1/tokens', verb='CREATE'):
        super().login(
            form=dict(email=email, password=password),
            url=url,
            verb=verb
        )


class RandomMonkeyPatch:
    """
    For faking the random function
    """

    fake_random = None

    def __init__(self, fake_random):
        self.__class__.fake_random = fake_random

    @staticmethod
    def random(size):
        return RandomMonkeyPatch.fake_random[:size]

    def __enter__(self):
        self.real_random = cryptohelpers.random
        cryptohelpers.random = RandomMonkeyPatch.random

    def __exit__(self, exc_type, exc_val, exc_tb):
        cryptohelpers.random = self.real_random

