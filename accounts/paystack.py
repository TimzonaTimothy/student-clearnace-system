from django.conf import settings
import requests


def BankList():
    SECRET_KEY = settings.PAYSTACK_PRIVATE_KEY
    base_url = 'https://api.paystack.co/bank'

    header = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content_type": 'Application/json',
        }
    param = {
        "country": 'nigeria',
        "currency":'NGN',
        "perPage": 50,
    }

    response =  requests.get(base_url, headers=header, params=param)

    if response.status_code == 200:
            response_data = response.json()
            return response_data['data']

 

def InitiatingTransfer(account_name, account_no, bank_code):
    SECRET_KEY = settings.PAYSTACK_PRIVATE_KEY
    base_url = 'https://api.paystack.co/transferrecipient'

    header = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content_type": 'Application/json',
        }
    Data = {
        "type": "nuban",
        "name": account_name,
        "account_number": account_no,
        "bank_code": bank_code,
    }

    response =  requests.post(base_url, data=Data, headers=header)

    if response.status_code == 201 or response.status_code ==200:
        response_data = response.json()
        return response_data['data']
    response_data = response.json()
    return response.status_code

def MakePayment(amount, recipient_code):
    SECRET_KEY = settings.PAYSTACK_PRIVATE_KEY
    base_url = 'https://api.paystack.co/transfer'

    header = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content_type": 'Application/json',
        }
    Data = {
        "source":"balance",
        "amount": amount,
        "recipient": recipient_code,
        "reason": "Balance Withdrawal",
    }

    response =  requests.post(base_url, data=Data, headers=header)

    if response.status_code == 201 or response.status_code ==200:
        response_data = response.json()
        return response_data['data']
    response_data = response.json()
    return response.status_code,response_data

            
def VerifyAccount(account, code):
    SECRET_KEY = settings.PAYSTACK_PRIVATE_KEY
    base_url = 'https://api.paystack.co/bank/resolve'

    header = {
            "Authorization": f"Bearer {SECRET_KEY}",
            "Content_type": 'Application/json',
        }
    param = {
        "account_number": account,
        "bank_code": code,
    }

    response =  requests.get(base_url, headers=header, params=param)

    if response.status_code == 200:
            response_data = response.json()
            return response_data['data']
                        
            


class PayStackPayment():
    SECRET_KEY = settings.PAYSTACK_PRIVATE_KEY
    base_url = 'https://api.paystack.co'

    def verify_payment(self, reference, *arg, **kwargs):
        path = f"/transaction/verify/{reference}"
        
        header = {
            "Authorization": f"Bearer {self.SECRET_KEY}",
            "Content_type": 'Application/json',
        }
        url =self.base_url + path
        response =  requests.get(url, headers=header)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        response_data = response.json()
        return response_data['status'], response_data['message']