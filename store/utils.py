import random
import string
from . import checksum
from django.conf import settings
import requests
import json



def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    order_new_id = random_string_generator()

    Token = instance.__class__

    qs_exists = Token.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_new_id


def VerifyPaytmResponse(response):
    response_dict = {}
    if response.method == "POST":
        data_dict = {}
        for key in response.POST:
            data_dict[key] = response.POST[key]
        MID = data_dict['MID']
        ORDERID = data_dict['ORDERID']
        verify = checksum.verify_checksum(data_dict, settings.PAYTM_MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            STATUS_URL = settings.PAYTM_TRANSACTION_STATUS_URL
            headers = {
                'Content-Type': 'application/json',
            }
            data = '{"MID":"%s","ORDERID":"%s"}'%(MID, ORDERID)
            check_resp = requests.post(STATUS_URL, data=data, headers=headers).json()
            if check_resp['STATUS']=='TXN_SUCCESS':
                response_dict['verified'] = True
                response_dict['paytm'] = check_resp
                return (response_dict)
            else:
                response_dict['verified'] = False
                response_dict['paytm'] = check_resp
                return (response_dict)
        else:
            response_dict['verified'] = False
            return (response_dict)
    response_dict['verified'] = False
    return response_dict