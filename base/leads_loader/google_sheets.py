import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from .lead_loader_base import LeadLoaderBase

# Set the scopes for Google API for using Google Sheets as CRM
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_google_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

class GoogleSheetLeadLoader(LeadLoaderBase):
    def __init__(self, spreadsheet_id, sheet_name=None):
        self.sheet_service = build("sheets", "v4", credentials=get_google_credentials())
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name or self._get_sheet_name_from_id()

    def fetch_records(self, lead_ids=None, status="NEW"):
        """
        Fetches leads from Google Sheets. If lead IDs are provided, fetch those specific records.
        Otherwise, fetch leads matching the given status.
        """
        try:
            result = self.sheet_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, range=self.sheet_name
            ).execute()
            rows = result.get("values", [])
            headers = rows[0]
            records = []

            for i, row in enumerate(rows[1:], start=2):  # Start from row 2 for data
                record = dict(zip(headers, row))
                record["id"] = f"{i}"  # Add row number as an ID
                
                formatted_record = {
                    "id": record["id"],
                    "first name": record.get("First Name", ""),
                    "last name": record.get("Last Name", ""),
                    "email": record.get("Email", ""),
                    "address": record.get("Address", ""),
                    "phone": record.get("Phone", "")
                }

                if lead_ids:
                    if record["id"] in lead_ids:
                        records.append(formatted_record)
                elif record.get("Status") == status:
                    records.append(formatted_record)
            return records
        except HttpError as e:
            print(f"Error fetching records from Google Sheets: {e}")
            return []

    def update_record(self, lead_id, updates: dict):
        """
        Updates a record in Google Sheets, adding or modifying specified fields.

        Args:
            lead_id (int): The row number of the record to update.
            updates (dict): A dictionary of fields to update or add.

        Returns:
            dict: The updated record ID and fields if successful, None otherwise.
        """
        try:
            # Fetch the header row to identify column indices
            result = self.sheet_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, range=self.sheet_name
            ).execute()
            rows = result.get("values", [])
            headers = rows[0]

            # Prepare the update body for all specified fields
            updates_batch = []
            for field, value in updates.items():
                if field in headers:
                    col_index = headers.index(field)
                    col_letter = chr(65 + col_index)  # Convert index to column letter
                    range_ = f"{self.sheet_name}!{col_letter}{lead_id}"
                    updates_batch.append({
                        "range": range_,
                        "values": [[value]],
                    })

            # Execute batch update for efficiency
            if updates_batch:
                body = {"valueInputOption": "RAW", "data": updates_batch}
                self.sheet_service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()
            return {"id": lead_id, "updated_fields": updates}
        except HttpError as e:
            print(f"Error updating Google Sheets record: {e}")
            return None

    def update_records_batch(self, leads):
        """
        Updates multiple records in Google Sheets based on a list of Lead objects.
        """
        updated_records = []
        for lead in leads:
            try:
                updated_record = self.update_record(lead['id'], lead['updates'])
                if updated_record:
                    updated_records.append(updated_record)
            except Exception as e:
                print(f"Skipping lead ID {lead['id']}: {e}")
        return updated_records

    def _get_sheet_name_from_id(self):
        """
        Retrieves the default sheet name if not explicitly provided.
        """
        try:
            result = self.sheet_service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = result.get("sheets", [])
            if not sheets:
                raise ValueError("No sheets found in the spreadsheet.")
            return sheets[0]["properties"]["title"]  # Default to the first sheet
        except HttpError as e:
            print(f"Error fetching sheet name: {e}")
            raise
