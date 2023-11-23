import requests

response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=68cfcf7e3e554734a0364618fa606998&email=edwardprosper001@gmail.com")
print(response.status_code)
print(response.content)