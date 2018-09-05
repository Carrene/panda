from restfulpy.testing import ApplicableTestCase

from panda import Panda, cryptohelpers


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda

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

