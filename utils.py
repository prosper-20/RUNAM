import requests
from decouple import config
# import requests

# response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=68cfcf7e3e554734a0364618fa606998&email=edwardprosper00@gmail.com")
# print(response.status_code)
# print(response.content)

# response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=c2069a02bcba4f23984a9cf56677cb40")
# print(response.status_code)
# print(response.content)
# print("Done")


def verify_email(email):
    response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key={config('ABSTRACT_API_KEY')}&email={email}")
    dictionary_response = dict(response.json())
    if dictionary_response.get("deliverability") == "DELIVERABLE":
        return True
    return False








