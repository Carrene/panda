from bddrest.authoring import status, response

from .helpers import LocalApplicationTestCase


class TestMember(LocalApplicationTestCase):

    def test_metadata(self):
        with self.given(
            'Test metadata verb',
            '/apiv1/members',
            'METADATA'
        ):
            fields = response.json['fields']

            assert status == 200

            assert fields['email']['pattern'] is not None
            assert fields['email']['patternDescription'] is not None
            assert fields['email']['notNone'] is not None
            assert fields['email']['required'] is not None
            assert fields['email']['label'] is not None
            assert fields['email']['name'] is not None
            assert fields['email']['example'] is not None
            assert fields['email']['watermark'] is None
            assert fields['email']['minLength'] is not None
            assert fields['email']['maxLength'] is not None

            assert fields['title']['pattern'] is not None
            assert fields['title']['patternDescription'] is not None
            assert fields['title']['notNone'] is not None
            assert fields['title']['required'] is not None
            assert fields['title']['label'] is not None
            assert fields['title']['name'] is not None
            assert fields['title']['example'] is not None
            assert fields['title']['watermark'] is None
            assert fields['title']['minLength'] is not None
            assert fields['title']['maxLength'] is not None

            assert fields['password']['pattern'] is not None
            assert fields['password']['patternDescription'] is not None
            assert fields['password']['notNone'] is not None
            assert fields['password']['required'] is not None
            assert fields['password']['label'] is not None
            assert fields['password']['name'] is not None
            assert fields['password']['example'] is not None
            assert fields['password']['watermark'] is None
            assert fields['password']['minLength'] is not None
            assert fields['password']['maxLength'] is not None

            assert fields['firstName']['pattern'] is not None
            assert fields['firstName']['patternDescription'] is not None
            assert fields['firstName']['required'] is not None
            assert fields['firstName']['label'] is not None
            assert fields['firstName']['name'] is not None
            assert fields['firstName']['example'] is not None
            assert fields['firstName']['watermark'] is None
            assert fields['firstName']['minLength'] is not None
            assert fields['firstName']['maxLength'] is not None
            assert fields['firstName']['notNone'] is not None

            assert fields['lastName']['pattern'] is not None
            assert fields['lastName']['patternDescription'] is not None
            assert fields['lastName']['required'] is not None
            assert fields['lastName']['label'] is not None
            assert fields['lastName']['name'] is not None
            assert fields['lastName']['example'] is not None
            assert fields['lastName']['watermark'] is None
            assert fields['lastName']['minLength'] is not None
            assert fields['lastName']['maxLength'] is not None
            assert fields['lastName']['notNone'] is not None

            assert fields['phone']['pattern'] is not None
            assert fields['phone']['patternDescription'] is not None
            assert fields['phone']['required'] is not None
            assert fields['phone']['label'] is not None
            assert fields['phone']['name'] is not None
            assert fields['phone']['example'] is not None
            assert fields['phone']['watermark'] is None
            assert fields['phone']['minLength'] is not None
            assert fields['phone']['maxLength'] is not None
            assert fields['phone']['notNone'] is not None

            assert fields['avatar']['protected'] is not None
            assert fields['avatar']['notNone'] is not None
            assert fields['avatar']['label'] is not None
            assert fields['avatar']['required'] is not None

