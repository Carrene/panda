# pragma: no cover

import requests
import ujson
from kavenegar import APIException, HTTPException, KavenegarAPI
from nanohttp import settings, HTTPStatus


class SmsProvider:  # pragma: no cover
    def send(self, to_number, text):
        NotImplementedError()


class CmSmsProvider(SmsProvider):  # pragma: no cover
    def send(self, to_number, text):
        headers = {'Content-Type': 'application/json'}
        data = {
            "messages": {
                "authentication": {"productToken": settings.sms.cm.token},
                "msg": [{
                        "body": {"content": text},
                        "from": settings.sms.cm.sender,
                        "to": [{"number": f'{to_number}'}],
                        "reference": settings.sms.cm.refrence
                }]
            }
        }
        data = ujson.dumps(data)

        try:
            response = requests.post(
                settings.sms.cm.url,
                data=data,
                headers=headers
            )
        except(requests.exceptions.RequestException):
            raise HTTPStatus('800 SMS Provider Internal Error')


class IranSmsProvider(SmsProvider):  # pragma: no cover
    def send(self, to_number, text):
        try:
            api = KavenegarAPI(settings.sms.kavenegar.apiKey)
            params = {
                'sender': '',  # optional
                'receptor': str(to_number),
                'message': text,
            }
            api.sms_send(params)
        except(APIException, HTTPException):
            raise HTTPStatus('800 SMS Provider Internal Error')


class AutomaticSmsProvider(SmsProvider):  # pragma: no cover
    __real_sms_provider = None
    __iran_sms_provider = None

    @property
    def real_sms_provider(self):
        if not self.__real_sms_provider:
            self.__real_sms_provider = CmSmsProvider()
        return self.__real_sms_provider

    @property
    def iran_sms_provider(self):
        if not self.__iran_sms_provider:
            self.__iran_sms_provider = IranSmsProvider()
        return self.__iran_sms_provider

    def send(self, to_number, text):
        if str(to_number).startswith('98'):
            self.iran_sms_provider.send(to_number=to_number, text=text)
        else:
            self.real_sms_provider.send(to_number=to_number, text=text)


class ConsoleSmsProvider(SmsProvider):  # pragma: no cover
    def send(self, to_number, text):
        print(
            'SMS send request received for number : %s with text : %s' %
            (to_number, text)
        )

