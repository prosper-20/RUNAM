from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com
account_sid = "AC02833859030a4bc3b5c854c92351470e"
auth_token = "6956886edf86eaf87b5723674f6ed5ec"
client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+2349036356792",
    from_="+15017250604",
    body="Hello from Python!")

print(message.sid)