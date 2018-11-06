from bddrest.authoring import status, response

from panda.tests.helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

    def test_metadata(self):
        with self.given(
            'Test metadata verb',
            '/apiv1/organizations',
            'METADATA'
        ):
            fields = response.json['fields']

            assert status == 200

            assert fields['name']['pattern'] is not None
            assert fields['name']['pattern_description'] is not None
            assert fields['name']['required'] is not None
            assert fields['name']['label'] is not None
            assert fields['name']['name'] is not None
            assert fields['name']['example'] is not None
            assert fields['name']['watermark'] is not None
            assert fields['name']['minLength'] is not None
            assert fields['name']['maxLength'] is not None
            assert fields['name']['not_none'] is not None

