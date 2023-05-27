import vonage
import random

def generate_random_digits():
    return random.randint(1000, 9999)

ans = print(generate_random_digits)

client = vonage.Client(key="7f545860", secret="Naapq9dkmVRIgu9z")
sms = vonage.Sms(client)


responseData = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": "2349036356792",
        # "text": "A text message sent using the Nexmo SMS API",
        "text": f"{ans}"
    }
)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")