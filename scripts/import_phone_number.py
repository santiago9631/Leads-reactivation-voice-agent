import os
from base.voice_agent_providers.vapi import VapiAI
from dotenv import load_dotenv

load_dotenv()


twilio_number_config = {
    "provider": "twilio",
    "name": "My Phone Number",
    "number": os.getenv("TWILIO_PHONE_NUMBER"),
    "twilioAccountSid": os.getenv("TWILIO_ACCOUNT_SID"),
    "twilioAuthToken": os.getenv("TWILIO_AUTH_TOKEN")
}


# Import your Twilio phone number to Vapi
vapi_client = VapiAI()
output = vapi_client.add_phone_number(twilio_number_config)
print(output)
