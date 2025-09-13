from pyairtable import Table
from pyairtable.formulas import match
from .lead_loader_base import LeadLoaderBase

class AirtableLeadLoader(LeadLoaderBase):
    def __init__(self, access_token, base_id, table_name):
        # Use the access_token instead of api_key
        self.table = Table(access_token, base_id, table_name)

    def fetch_records(self, lead_ids=None, status="NEW"):
        """
        Fetches leads from Airtable. If lead IDs are provided, fetch those specific records.
        Otherwise, fetch leads matching the given status.
        """
        if lead_ids:
            leads = []
            for lead_id in lead_ids:
                record = self.table.get(lead_id)
                if record:
                    leads.append({
                        "id": record["id"],
                        "first name": record["fields"].get("First Name", ""),
                        "last name": record["fields"].get("Last Name", ""),
                        "email": record["fields"].get("Email"),
                        "address": record["fields"].get("Address", ""),
                        "phone": record["fields"].get("Phone", "")
                    })
            return leads
        else:
            # Fetch leads by status filter
            records = self.table.all(formula=match({"Status": status}))
            return [
                {
                    "id": record["id"],
                    "first name": record["fields"].get("First Name", ""),
                    "last name": record["fields"].get("Last Name", ""),
                    "email": record["fields"].get("Email"),
                    "address": record["fields"].get("Address", ""),
                    "phone": record["fields"].get("Phone", "")
                }
                for record in records
            ]


    def update_record(self, lead_id, updates: dict):
        """
        Updates a record in Airtable, adding new fields dynamically if they don't exist.

        Args:
            lead_id (str): The ID of the record to update.
            updates (dict): A dictionary of fields to update or add.
        
        Returns:
            dict: The updated record from Airtable.
        """
        # Fetch the current record to ensure it exists and get its fields
        record = self.table.get(lead_id)
        if not record:
            raise ValueError(f"Record with ID {lead_id} not found.")
        
        # Merge current fields with updates, adding any new fields
        current_fields = record.get("fields", {})
        updated_fields = {**current_fields, **updates}

        # Update the record in Airtable
        return self.table.update(lead_id, updated_fields)
    
    def update_records_batch(self, leads):
        """
        Updates multiple records in Airtable based on a list of Lead objects.
        """
        updated_records = []
        for lead in leads:
            try:
                lead_id = lead['id']
                record = self.table.get(lead_id)
                
                # Merge current fields with updates, adding any new fields
                current_fields = record.get("fields", {})
                updated_fields = {**current_fields, **lead['updates']}
                updated_record = self.update_record(lead['id'], updated_fields)
                updated_records.append(updated_record)
            except ValueError as e:
                print(f"Skipping lead ID {lead['id']}: {e}")

        return updated_records