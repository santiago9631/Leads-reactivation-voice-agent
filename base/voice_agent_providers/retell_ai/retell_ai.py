import os
import json
from ..base_agent import BaseAgent
from retell import Retell

class RetellAI(BaseAgent):
    def __init__(self, tools: dict):
        """
        Initialize the Retell AI client using the API key from the environment variable.
        """
        self.client = Retell(api_key=os.getenv("RETELL_API_KEY"))
        self.allowed_tools = tools
        
    async def make_call(self, request: dict):
        """
        Create a call via Vapi.
        """
        response = await self.client.call.create_phone_call(**request)
        return response
    
    async def handle_webhook_call(self, request: dict):
        try:
            post_data = await request.json()            
            event = post_data.get("event", "")
            print(post_data)
            
            # Verify signature
            valid_signature = self._validate_webhook(post_data)
            if not valid_signature:
                return {"status_code": 401, "content": {"message": "Unauthorized"}}
            
            if event != "":
                self._handle_retell_event(event, post_data)
            else: # This is a function call
                output = self._handle_tool_call()
                return output

        except Exception as err:
            print(f"Error in webhook: {err}")
            return {"status_code": 500, "content": {"message": "Internal Server Error"}}
        
    def get_allowed_tools(self):
        return self.allowed_tools

    def create_agent(self, config: str):
        response = self.client.agent.create(**config)
        return response
    
    def update_agent(self, agent_id: str, config: dict):
        response = self.client.agent.update(agent_id=agent_id, **config)
        return response

    def create_llm(self, config: dict):
        response = self.client.llm.create(**config)
        return response
    
    def update_llm(self, llm_id: str, config: dict):
        response = self.client.llm.update(llm_id=llm_id, **config)
        return response

    def add_phone_number(self, config: str):
        phone_number_response = self.client.phone_number.import_(**config)
        return phone_number_response
    
    # Perform any necessary search or modification on the leads before making the call
    def pre_call_processing(self, payload):
        pass
    
    # Build the call payload with all required information 
    def get_call_input_params(self, payload):
        pass
    
    # Process the end of call outputs and extract all relevant fields
    def process_call_outputs(self, payload):
        pass
       
    # Post call analysis: 
    # - Evaluate the call to determine lead qualification or interest
    # - Save data into your database or CRM
    def post_call_processing(self, payload):
        pass

    def _validate_webhook(self, data):
        # Verify signature
        valid_signature = self.client.verify(
            json.dumps(data, separators=(",", ":"), ensure_ascii=False),
            api_key=str(os.getenv("RETELL_API_KEY")),
            signature=str(data.get("headers", {}).get("X-Retell-Signature")),
        )
        if not valid_signature:
            print(
                "Received Unauthorized",
                data["event"],
                data["data"]["call_id"],
            )
        return valid_signature
    
    def _handle_retell_event(self, event, data):
        if event == "call_started":
            print("Call started event", data["data"]["call_id"])
        elif event == "call_ended":
            print("Call ended event", data["data"]["call_id"])
        elif event == "call_analyzed":
            print("Call analyzed event", data["data"]["call_id"])
            
            # Post call analysis and Update CRM
            call_output = self.process_call_outputs(data["data"])
            self.post_call_processing(call_output)
        else:
            print("Unknown event", event)
    
    async def _handle_tool_call(self, data):
        # Extract function name and arguments
        function_name = data.get("name")
        args = data.get("args", {})
        
        # Check if the function exists and call it
        if function_name in self.allowed_tools:
            result = await self.allowed_tools[function_name](**args)
            return {"name": function_name, "result": result}
        else:
            return {"name": function_name, "result": "Unknown function"}
            
    
            
        