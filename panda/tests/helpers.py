from restfulpy.testing import ApplicableTestCase

from panda import Panda


class LocadApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda

