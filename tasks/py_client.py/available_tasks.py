import requests

endpoint = "http://127.0.0.1:8000/tasks/available/"

token_endpoint = "http://127.0.0.1:8000/api/token/"

authentication_response = requests.post(token_endpoint, json={"email":"edwardprosper001@gmail.com", "password":"testing321"})
print(authentication_response.json())

if authentication_response.status_code == 200:

    token = authentication_response.json()["access"]
    headers = {
        "Authorization": f"Bearer {token}"
    }

    tasks_response = requests.get(endpoint, headers=headers)
    print(tasks_response.json())


else:
    print("Authentication credentials are invalid") 



