from .retell_ai import RetellAI
from dotenv import load_dotenv

load_dotenv()

agent_config = {
    "response_engine": {
        "type": "retell-llm",  # Required: Available option is 'retell-llm'
        "llm_id": "your_llm_id_here"  # Required: ID of the Retell LLM
    },
    "voice_id": "your_voice_id_here",  # Required: Unique voice ID
    "agent_name": None,  # Optional: Agent name for reference
    "voice_model": None,  # Optional: Voice model (e.g., 'eleven_turbo_v2')
    "fallback_voice_ids": None,  # Optional: Fallback voice IDs
    "voice_temperature": 1,  # Default: 1 (range: 0-2)
    "voice_speed": 1,  # Default: 1 (range: 0.5-2)
    "volume": 1,  # Default: 1 (range: 0-2)
    "responsiveness": 1,  # Default: 1 (range: 0-1)
    "interruption_sensitivity": 1,  # Default: 1 (range: 0-1)
    "enable_backchannel": False,  # Default: Disabled
    "backchannel_frequency": 0.8,  # Default: 0.8 (applies only if backchannel is enabled)
    "backchannel_words": None,  # Optional: List of backchannel words
    "reminder_trigger_ms": 10000,  # Default: 10000 ms (10 seconds)
    "reminder_max_count": 1,  # Default: 1 reminder
    "ambient_sound": None,  # Optional: Ambient sound type (e.g., 'coffee-shop')
    "ambient_sound_volume": 1,  # Default: 1 (range: 0-2)
    "language": "en-US",  # Default: 'en-US', options include multilingual support
    "webhook_url": None,  # Optional: Webhook URL for call events
    "boosted_keywords": None,  # Optional: Keywords for transcription bias
    "enable_transcription_formatting": True,  # Default: True
    "opt_out_sensitive_data_storage": False,  # Default: False
    "pronunciation_dictionary": None,  # Optional: Pronunciation guide
    "normalize_for_speech": True,  # Default: True
    "end_call_after_silence_ms": 600000,  # Default: 600000 ms (10 minutes)
    "max_call_duration_ms": 3600000,  # Default: 3600000 ms (1 hour)
    "enable_voicemail_detection": False,  # Default: Disabled
    "voicemail_message": "",  # Default: Empty string (message to play for voicemail)
    "voicemail_detection_timeout_ms": 30000,  # Default: 30000 ms (30 seconds)
    "post_call_analysis_data": [  # Optional: Post-call analysis variables
        {
            "type": "string",  # Required: Type of variable (only 'string' supported)
            "name": "example_variable_name",  # Required: Name of the variable
            "description": "Description of the variable",  # Required: Description
            "examples": ["Example value 1", "Example value 2"]  # Optional examples
        }
    ]
}

retell_client = RetellAI()

# Create a new agent using the above config
output = retell_client.create_agent(agent_config)
print(output)


# Update an existing agent with the above config
# agent_id = ""
# output = retell_client.update_agent(agent_id, agent_config)
# print(output)