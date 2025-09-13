import os
from base.voice_agent_providers.vapi import VapiAI
from dotenv import load_dotenv

load_dotenv()

tool_config = {
    "type": "function",
    "messages": [
        {
            "type": "request-start",
            "content": "Alright, let me book your appointment. This will just take a moment."
        },
        {
            "type": "request-complete",
            "content": "Great news! Your appointment is confirmed. Is there anything else I can help you with?"
        },
        {
            "type": "request-failed",
            "content": "I’m sorry, I couldn’t book the appointment at this time. Let’s try again in a moment, or I can assist you with something else."
        },
        {
            "type": "request-response-delayed",
            "content": "It’s taking a bit longer than usual to confirm your appointment. Thanks for your patience, I’ll update you shortly.",
            "timingMilliseconds": 2000
        }
    ],
    "function": {
        "name": "bookAppointment",
        "parameters": {
            "type": "object",
            "properties": {
                "Name": {"type": "string"},
                "PhoneNumber": {"type": "string"},
                "PreferredDateTime": {"type": "string"}
            },
            "required": ["Name", "PhoneNumber", "EmailAddress", "PreferredDateTime"]
        },
        "description": "Books an appointment with the provided client details."
    },
    "async": False,
    "server": {
        "url": f"{os.getenv("SERVER_URL")}/webhook"
    }
}

vapi_client = VapiAI()

# Create a new tool with the above config
output = vapi_client.create_tool(tool_config)
print(output)

# Get the tool id, necessary for creating/updating assistant
print(output["id"])


# Update an existing tool with the above config
# tool_id = ""
# output = vapi_client.update_tool(tool_id, tool_config)
# print(output)