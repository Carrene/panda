from os import path

from restfulpy.testing import ApplicableTestCase

from panda import Panda, cryptohelpers
from panda.models import Application, Member


HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')
    __metadata__ = {
        r'^/apiv1/applications.*': Application.json_metadata()['fields'],
        r'^/apiv1/members.*': Member.json_metadata()['fields'],
        r'^/apiv1/passwords.*': dict(
            currentPassword=dict(type='str', required=True, not_none=True),
            newPassword=dict(type='str', required=True, not_none=True),
        ),
        r'^/apiv1/resetpasswordtokens.*': dict(
            email=dict(type='str', required=True, not_none=True),
        ),
        r'^/apiv1/accesstokens.*': dict(
            code=dict(type='str', required=True, not_none=True),
            secret=dict(type='str', required=True, not_none=True),
            applicationId=dict(type='int', required=True, not_none=True),
        ),
        r'^/apiv1/authorizationcodes.*': dict(
            scopes=dict(type='str', required=True, not_none=True),
            applicationId=dict(type='int', required=True, not_none=True),
            state=dict(type='str', required=False, not_none=False),
            redirectUri=dict(type='str', required=False, not_none=False),
        ),
         r'^/apiv1/emails.*': dict(
            email=dict(type='str', required=True, not_none=True),
        ),
        r'^/apiv1/tokens.*': dict(
            email=dict(type='str', required=True, not_none=True),
            password=dict(type='str', required=True, not_none=True),
        ),
        r'^/apiv1/phonenumbers.*': dict(
            activationCode=dict(type='str', required=True, not_none=True),
            activationToken=dict(type='str', required=True, not_none=True),
        ),
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

