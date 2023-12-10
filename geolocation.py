import requests
from decouple import config

api_key = 'YOUR_API_KEY'
api_url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={config('ABSTRACT_API_GEOLOCATION_KEY')}"


def get_ip_geolocation_data(ip_address):
   print(ip_address)
   response = requests.get(api_url)
   return response.content



url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={config('ABSTRACT_API_GEOLOCATION_KEY')}"

response = requests.request("GET", url)

# print(response.text)