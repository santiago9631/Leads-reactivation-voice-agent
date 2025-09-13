from .retell_ai import RetellAI
from dotenv import load_dotenv

load_dotenv()


phone_number_config = {
    "phone_number": "+1234567890",  # Required: E.164 format (+country code, number)
    "termination_uri": "example.pstn.twilio.com",  # Required: Elastic SIP trunk URI
    "sip_trunk_auth_username": None,  # Optional: SIP trunk authentication username
    "sip_trunk_auth_password": None,  # Optional: SIP trunk authentication password
    "inbound_agent_id": None,  # Optional: Agent ID for inbound calls
    "outbound_agent_id": None,  # Optional: Agent ID for outbound calls
    "nickname": "My Phone Number"  # Optional: Nickname for reference
}


# Import your Twilio phone number to Retell account
# Must include your number and the termination URI you get from Twilio
retell_client = RetellAI()
phone_number_response = retell_client.add_phone_number(phone_number_config)
print(phone_number_response)
