import os
from vapi import Vapi
from ..base_agent import BaseAgent


class VapiAI(BaseAgent):
    def __init__(self, tools: dict):
        self.client = Vapi(token=os.getenv("VAPI_API_KEY"))
        self.allowed_tools = tools

    async def make_call(self, request: dict):
        print(f"Making a Vapi call")
        response = self.client.calls.create(**request)
        return response
    
    async def handle_webhook_call(self, request: dict):
        # Parse the JSON payload from the request
        payload = await request.json()
        
        if payload['type']['message'] == "tool-calls":
            response = await self.tools_call_handler(payload)
        elif payload['type']['message'] == "end-of-call-report":
            response = await self.end_of_call_report_handler(payload)
        else:
            pass
        
        return response

    def create_agent(self, request: dict):
        """
        Create an assistant/agent via Vapi.
        
        Args:
            request (dict): A dictionary containing all required parameters.
        """
        print("Vapi creating assistant.")
        output = self.client.assistants.create(**request)
        return {"status": "success", "details": output}

    def update_agent(self, agent_id: str, request: dict):
        """
        Update an existing assistant/agent via Vapi.
        """
        print("Vapi updating assistant.")
        output = self.client.assistants.update(id=agent_id, **request)
        return {"status": "success", "details": output}

    def create_tool(self, request: dict):
        """
        Create a tool in Vapi.
        
        Args:
            request (dict): A dictionary containing all required parameters.
        """
        print("Vapi creating tool.")
        tool_creation_output = self.client.tools.create(request=request)
        return {"status": "success", "details": tool_creation_output}

    def update_tool(self, tool_id: str, request: dict):
        """
        Update an existing tool in Vapi.
        """
        print("Updating Vapi tool")
        tool_id = request.pop("id", None)
        if not tool_id:
            raise ValueError("The 'id' field is required to update a tool.")
        output = self.client.tools.update(id=tool_id, request=request)
        return {"status": "success", "details": output}

    def add_phone_number(self, request: dict):
        """
        Add a phone number to Vapi.
        
        Args:
            request (dict): A dictionary containing all required parameters.
        """
        print("Adding phone number in Vapi")
        phone_creation_output = self.client.phone_numbers.create(request=request)
        return {"status": "success", "details": phone_creation_output}
    
    def get_allowed_tools(self):
        return self.allowed_tools
    
    async def tools_call_handler(self, payload):
        results = []
        tool_call_list = payload.get('toolCallList')
        
        for tool_call in tool_call_list:
            call_id = tool_call.get("id")
            function_call = tool_call.get("function")
            name = function_call.get('name')
            arguments = function_call.get('arguments')
            
            if name in self.allowed_tools:
                result = await self.allowed_tools[name](**arguments)
                results.append({
                    "name": name,
                    "toolCallId": call_id,
                    "result": result
                })
            else:
                results.append({
                    "name": name,
                    "toolCallId": call_id,
                    "result": "Uknown function"
                })

        return {"results": results}
    
    async def end_of_call_report_handler(self, payload):
        call_output = self.process_call_outputs(payload)
        self.post_call_processing(call_output)
        
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