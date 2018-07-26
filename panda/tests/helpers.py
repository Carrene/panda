from restfulpy.testing import ApplicableTestCase

from panda import Panda


class LoadApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda

