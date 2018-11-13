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

            assert fields['title']['pattern'] is not None
            assert fields['title']['pattern_description'] is not None
            assert fields['title']['required'] is not None
            assert fields['title']['label'] is not None
            assert fields['title']['name'] is not None
            assert fields['title']['example'] is not None
            assert fields['title']['watermark'] is not None
            assert fields['title']['minLength'] is not None
            assert fields['title']['maxLength'] is not None
            assert fields['title']['not_none'] is not None

            assert fields['url']['pattern'] is not None
            assert fields['url']['pattern_description'] is not None
            assert fields['url']['required'] is not None
            assert fields['url']['label'] is not None
            assert fields['url']['name'] is not None
            assert fields['url']['example'] is not None
            assert fields['url']['watermark'] is not None
            assert fields['url']['minLength'] is not None
            assert fields['url']['maxLength'] is not None
            assert fields['url']['not_none'] is not None

            assert fields['domain']['pattern'] is not None
            assert fields['domain']['pattern_description'] is not None
            assert fields['domain']['required'] is not None
            assert fields['domain']['label'] is not None
            assert fields['domain']['name'] is not None
            assert fields['domain']['example'] is not None
            assert fields['domain']['watermark'] is not None
            assert fields['domain']['minLength'] is not None
            assert fields['domain']['maxLength'] is not None
            assert fields['domain']['not_none'] is not None

            assert fields['icon']['protected'] is not None
            assert fields['icon']['not_none'] is not None
            assert fields['icon']['label'] is not None
            assert fields['icon']['required'] is not None

