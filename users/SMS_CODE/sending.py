# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC02833859030a4bc3b5c854c92351470e"
auth_token = "6956886edf86eaf87b5723674f6ed5ec"
client = Client(account_sid, auth_token)
message = client.messages.create(
  body="Hello from Twilio",
  from_="+12708123914",
  to="+2349036356792"
)
print(message.sid)