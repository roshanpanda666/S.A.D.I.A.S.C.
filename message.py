from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def sendmessage():
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+15076280790',  # Twilio sandbox number
        body='person is detected',
        to='+917608946420'     # Your recipient number
    )

    print(message.sid)
