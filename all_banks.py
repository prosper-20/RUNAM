import requests
from decouple import config

url="https://api.paystack.co/bank"

response = requests.get(url)

headers = {
    "Authorization": f"Bearer {config('')}"
}


