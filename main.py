import os
import time
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from base.leads_loader.airtable import AirtableLeadLoader
from src.vapi_automation import VapiAutomation
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = FastAPI()

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize leads loader (Airtable, Sheets, Hubspot or add your own custom CRM)
lead_loader = AirtableLeadLoader(
    access_token=os.getenv("AIRTABLE_ACCESS_TOKEN"),
    base_id=os.getenv("AIRTABLE_BASE_ID"),
    table_name=os.getenv("AIRTABLE_TABLE_NAME"),
)

# Get Vapi automation instance
automation = VapiAutomation(lead_loader)

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


@app.post("/execute")
async def execute(payload: dict):
    """
    Trigger the lead processing workflow. Payload should contain list of lead IDs.
    """
    try:
        # Fetch leads based on provided IDs
        lead_ids = payload.get("lead_ids", [])
        
        print("Fetching lead data...")
        leads = automation.load_leads(lead_ids=lead_ids)
        if not leads:
            return {"message": "No leads found."}
        
        for lead in leads:
            # Augment the lead data (web research, linkedIn profile,...) 
            automation.pre_call_processing(lead)
            
            # Structure the required call parameters in Vapi format
            call_params = automation.get_call_input_params(lead)
            
            # Initiate the call
            print(f"Calling Lead {lead['id']}...")
            automation.make_call(call_params)
            
            # await 1s
            time.sleep(1)

        return {"message": "Calls initiated successfully for all leads."}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while executing the workflow")

@app.post("/webhook")
async def handle_webhook(request: Request):
    """
    Handle incoming webhook requests dynamically.
    """
    try:
        response = await automation.handle_webhook_call(request)
        return response
    except Exception as e:
        print("Error processing webhook:", str(e))
        raise HTTPException(status_code=400, detail="Invalid webhook payload")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
