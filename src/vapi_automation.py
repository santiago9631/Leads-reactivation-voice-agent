import os
from src.voice_agent_providers.vapi.vapi_ai import VapiAI
from src.utils import get_current_date_time, calculate_duration_in_minutes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from .structured_io import CallAnalysisResponse, Lead
from .prompts import CALL_ANALYSIS_PROMPT
from .tools.calendar_tool import book_appointement


TOOLS = {
    "bookAppointment": book_appointement
}

class VapiAutomation(VapiAI):
    def __init__(self, lead_loader):
        """
        Initialize the class VapiAutomation class.

        Args:
            lead_loader: A lead loader instance for managing lead data.
        """
        super().__init__(tools=TOOLS)  # Initialize the base class
        self.lead_loader = lead_loader 
        
    def load_leads(self, lead_ids):
        raw_leads = self.lead_loader.fetch_records(lead_ids=lead_ids)
        if not raw_leads:
            return []
        
        # Structure the leads
        leads = [
            Lead(
                id=lead["id"],
                first_name=lead.get("first name", ""),
                last_name=lead.get("last name", ""),
                address=lead.get("address", ""),
                email=lead.get("email", ""),
                phone=lead.get("phone", ""),
            )
            for lead in raw_leads
        ]
        print(f"Loaded {len(leads)} leads: {leads}")
        
        return leads

    def pre_call_processing(self, payload):
        pass
       
    def get_call_input_params(self, lead_data: dict) -> dict:
        """
        Build the payload required to initiate a call via Vapi.

        Args:
            lead_data (dict): Lead data containing phone number and other details.
        
        Returns:
            dict: A formatted payload to pass to the Vapi call API.
        """
        return {
            "phone_number_id": os.getenv("VAPI_PHONE_ID"),
            "assistant_id": os.getenv("VAPI_ASSISTANT_ID"),
            "customer": {
                "number": lead_data["phone"],
            },
            "assistant_overrides": {
                "variable_values": {
                    "firstName": lead_data["first_name"],
                    "lastName": lead_data["last_name"],
                    "email": lead_data["email"],
                    "address": lead_data["address"],
                    "date": get_current_date_time()
                }
            }
        }

    def process_call_outputs(self, response: dict) -> dict:
        """
        Process the response from a Vapi call and extract relevant details.

        Args:
            response (dict): The raw response from the Vapi API.
        
        Returns:
            dict: Processed call outputs.
        """
        return {
            "call_id": response["call"]["id"],
            "status": response["call"]["status"],
            "duration": calculate_duration_in_minutes(
                response["startedAt"], response["endedAt"]
            ),
            "cost": response["cost"],
            "endedReason": response["endedReason"],
            "transcript": response["artifact"]["transcript"],
            "lead_info": response["call"]["assistantOverrides"]["variableValues"]
        }

    def evaluate_call(self, call_outputs: dict) -> dict:
        """
        Perform post-call analysis and update the CRM with the results.

        Args:
            call_outputs (dict): Processed call outputs.
        
        Returns:
            dict: Updated lead information.
        """
        # Prepare the analysis prompt for LLM
        call_analysis_prompt = ChatPromptTemplate.from_template(CALL_ANALYSIS_PROMPT)
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        structured_llm = llm.with_structured_output(CallAnalysisResponse)
        evaluate_call = call_analysis_prompt | structured_llm | JsonOutputParser()

        # Invoke LLM for analysis
        output = evaluate_call.invoke({
            "name": f"{call_outputs['lead_info']['firstName']} {call_outputs['lead_info']['lastName']}",
            "address": call_outputs['lead_info']['address'],
            "email": call_outputs['lead_info']['email'],
            "transcript": call_outputs['transcript']
        })

        # Update CRM, Make sure to use the correct field names
        updates = {
            "Status": "CONTACTED",
            "Call ID": call_outputs["call_id"],
            "Call Status": call_outputs["status"],
            "Duration": call_outputs["duration"],
            "Cost": call_outputs["cost"],
            "End Reason": call_outputs["endedReason"],
            "Transcript": call_outputs["transcript"],
            "Call Summary": output.get("call_summary"),
            "Interested": output.get("lead_interested"),
            "Comment": output.get("justification")
        }

        self.lead_loader.update_record(call_outputs["lead_info"]["id"], updates)

        return updates
