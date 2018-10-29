from bddrest.authoring import status, response

from panda.tests.helpers import LocalApplicationTestCase


class TestApplication(LocalApplicationTestCase):

    def test_metadata(self):
        with self.given(
            'Test metadata verb',
            '/apiv1/applications',
            'METADATA'
        ):
            fields = response.json['fields']

            assert status == 200

            assert fields['title']['label'] is not None
            assert fields['title']['maxLength'] is not None
            assert fields['title']['minLength'] is not None
            assert fields['title']['watermark'] is not None
            assert fields['title']['name'] is not None
            assert fields['title']['not_none'] is not None
            assert fields['title']['required'] is not None

            assert fields['redirectUri']['label'] is not None
            assert fields['redirectUri']['watermark'] is not None
            assert fields['redirectUri']['name'] is not None
            assert fields['redirectUri']['not_none'] is not None
            assert fields['redirectUri']['required'] is not None
            assert fields['redirectUri']['minLength'] is not None
            assert fields['redirectUri']['maxLength'] is not None

            assert fields['icon']['protected'] is not None
            assert fields['icon']['not_none'] is not None
            assert fields['icon']['label'] is not None
            assert fields['icon']['required'] is not None

