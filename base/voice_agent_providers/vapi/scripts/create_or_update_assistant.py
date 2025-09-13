from base.voice_agent_providers.vapi import VapiAI
from dotenv import load_dotenv

load_dotenv()

assistant_config = {
    "name": "Sandra",
    "transcriber": {
        "provider": "deepgram",  # Transcriber provider
        "language": "en"
    },
    "model": {
        "provider": "openai",  # Model provider
        "model": "gpt-4o",  # Model ID
        "toolIds": ["tool_id"],
        "messages": [
            {
                "role": "system",
                "content": "system prompt"
            }
        ]
    },
    "voice": {
        "provider": "openai",  # Voice provider
        "voiceId": "alloy"  # Voice ID
    },
    "first_message": "Hi, is this {{firstName}}?",
    "end_call_message": "Thanks for your time.",
    "analysis_plan": {
        "summaryPlan": {
            "messages": [],
            "enabled": False,
        },
        "structuredDataPlan": {
            "messages": [],
            "enabled": False,
        },
        "successEvaluationPlan": {
            "rubric": "NumericScale",
            "messages": [],
            "enabled": False
        }
    },
    "server_url": ""
}


vapi_client = VapiAI()

# Create a new assistant using the above config
output = vapi_client.create_agent(assistant_config)
print(output)


# Update an existing assistant with the above config
# assistant_id = ""
# output = vapi_client.update_agent(assistant_id, assistant_config)
# print(output)