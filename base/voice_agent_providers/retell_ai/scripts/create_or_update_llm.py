from .retell_ai import RetellAI
from dotenv import load_dotenv

load_dotenv()

llm_config = {
    "model": 'gpt-4o',  # Options: 'gpt-4o', 'gpt-4o-mini', 'claude-3.5-sonnet', 'claude-3-haiku'
    "s2s_model": None,  # Option: 'gpt-4o-realtime', can only set this or `model`, not both.
    "model_temperature": 0.3,  # Default is 0, range: [0, 1]
    "tool_call_strict_mode": False,  # Default is False
    "general_prompt": "Your prompt",  # General prompt appended to system prompt
    "general_tools": [
        {
            "type": "end_call",
            "name": "end_call",
            "description": "Used to end the call with the customer.",
        },
        {
            "type": "custom",
            "name": "bookAppointment",
            "url": "https://example.com/tool",  # URL that describes the tool
            "description": "Books an appointment with the provided client details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Name": {
                        "type": "string"
                    },
                    "PhoneNumber": {
                        "type": "string"
                    },
                    "PreferredDateTime": {
                        "type": "string"
                    }
                },
                "required": ["Name", "PhoneNumber", "PreferredDateTime"]
            },  # JSON Schema object
            "speak_during_execution": True,
            "speak_after_execution": True,
            "execution_message_description": "Alright, let me book your appointment. This will just take a moment.",
            "timeout_ms": 10000,  # Default timeout: 10s
        }
    ],
    "states": None,  # List of states if applicable, otherwise null
    "starting_state": None,  # Name of the starting state, required if states are defined
    "begin_message": "Hi, is this {{firstName}}?",  # Empty string means agent will wait for the user to speak first
    "inbound_dynamic_variables_webhook_url": None,  # Webhook URL for inbound dynamic variables
    "knowledge_base_ids": None,  # List of knowledge base IDs, or null to remove all
}

retell_client = RetellAI()

# Create a new Retell LLM with the above config
output = retell_client.create_llm(llm_config)
print(output)


# Update an existing RETELL LLM with the above config
# llm_id = ""
# output = retell_client.update_tool(llm_id, llm_config)
# print(output)