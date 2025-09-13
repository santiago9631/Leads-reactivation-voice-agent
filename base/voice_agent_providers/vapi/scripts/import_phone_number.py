from .vapi_ai import VapiAI
from dotenv import load_dotenv

load_dotenv()


twilio_number_config = {
    "provider": "twilio",
    "name": "Main Caller",
    "number": "",
    "twilioAccountSid": "",
    "twilioAuthToken": ""
}


# Import your Twilio phone number to Vapi
vapi_client = VapiAI()
output = vapi_client.add_phone_number(twilio_number_config)
print(output)
