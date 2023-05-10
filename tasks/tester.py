import requests
import base64

id = "F5B37620-0E3B-4153-B15D-AF2B5312C740"
api = "uiEOe6mA+CIkTHHgXQYz/yMiuxPKqV0waWyw8cCUj6nT1jD3RfKueFODZ3fg2PuvxlRKIx359tf7sogCRV4PIg=="
url = "https://rest-ww.telesign.com/v1/verify/sms"

my_string = f"{id}:{api}"

my_string.encode(encoding = 'UTF-8', errors = 'strict')
# message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(my_string)

print(my_string)
print(base64_bytes)

# payload = "is_primary=true"
# headers = {
#     "accept": "application/json",
#     "content-type": "application/x-www-form-urlencoded",
#     "authorization": "Basic RjVCMzc2MjAtMEUzQi00MTUzLUIxNUQtQUYyQjUzMTJDNzQwOnVpRU9lNm1BK0NJa1RISGdYUVl6L3lNaXV4UEtxVjB3YVd5dzhjQ1VqNm5UMWpEM1JmS3VlRk9EWjNmZzJQdXZ4bFJLSXgzNTl0Zjdzb2dDUlY0UElnPT0="
# }

# response = requests.post(url, data=payload, headers=headers)

# print(response.text)