import requests
from decouple import config

url="https://api.paystack.co/transaction/initialize"

def initiate_transaction(url):
    headers= {"Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}",
              "Content-Type": "application/json"}
    data={ 
        "email": "customer@email.com", 
        "amount": "20000"
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()

# print(initiate_transaction(url))


def verify_transaction(reference):
    url= f"https://api.paystack.co/transaction/verify/{reference}"
    headers= {"Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}",
              "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

# print(verify_transaction('os9ld5al1y'))


all_transactions_url="https://api.paystack.co/transaction"


def list_transactions(url):
    headers= {"Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}",
              "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()

# print(list_transactions(all_transactions_url))


def create_pay_with_transfer_charge():

    url="https://api.paystack.co/charge"
    headers= {"Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}",
                "Content-Type": "application/json"}
    data= { 
    "email": "another@one.com", 
    "amount": "25000", 
    "bank_transfer": {
        "account_expires_at": "2023-09-12T13:10:00Z"
    }
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

print(create_pay_with_transfer_charge())

