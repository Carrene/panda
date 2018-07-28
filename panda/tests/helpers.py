from restfulpy.testing import ApplicableTestCase

from panda import Panda
from panda.models import Member


class LoadApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Panda

