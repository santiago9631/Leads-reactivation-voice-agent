import os
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException
from .lead_loader_base import LeadLoaderBase

class HubSpotLeadLoader(LeadLoaderBase):
    def __init__(self, access_token=None):
        # Use access_token instead of environment variable for more flexibility
        self.client = hubspot.Client.create(access_token=access_token or os.getenv("HUBSPOT_API_KEY"))

    def fetch_records(self, lead_ids=None, status="NEW"):
        """
        Fetches leads from HubSpot. If lead IDs are provided, fetch those specific records.
        Otherwise, fetch leads matching the given status.
        """
        try:
            if lead_ids:
                leads = []
                for lead_id in lead_ids:
                    contact = self.client.crm.contacts.basic_api.get_by_id(
                        contact_id=lead_id,
                        properties=["email", "firstname", "lastname", "hs_lead_status", "address", "phone"]
                    )
                    if contact:
                        leads.append({
                            "id": contact.id,
                            "first name": contact.properties.get("firstname", ""),
                            "last name": contact.properties.get("lastname", ""),
                            "email": contact.properties.get("email"),
                            "address": contact.properties.get("address", ""),
                            "phone": contact.properties.get("phone", ""),
                            "status": contact.properties.get("hs_lead_status", "")
                        })
                return leads
            else:
                # Fetch leads by status filter
                api_response = self.client.crm.contacts.basic_api.get_page(
                    limit=100,
                    properties=["email", "firstname", "lastname", "hs_lead_status", "address", "phone"],
                    archived=False,
                )
                records = []
                for contact in api_response.results:
                    lead_status = contact.properties.get("hs_lead_status")
                    if lead_status == status:
                        records.append({
                            "id": contact.id,
                            "first name": contact.properties.get("firstname", ""),
                            "last name": contact.properties.get("lastname", ""),
                            "email": contact.properties.get("email"),
                            "address": contact.properties.get("address", ""),
                            "phone": contact.properties.get("phone", "")
                        })
                return records
        except ApiException as e:
            print(f"Error fetching records from HubSpot: {e}")
            return []

    def update_record(self, lead_id, updates: dict):
        """
        Updates a record in HubSpot, adding new fields dynamically if they don't exist.

        Args:
            lead_id (str): The ID of the record to update.
            updates (dict): A dictionary of fields to update or add.

        Returns:
            dict: The updated record ID and fields if successful, None otherwise.
        """
        try:
            # Prepare the fields to update in HubSpot
            simple_public_object_input = SimplePublicObjectInput(properties=updates)

            # Update the record in HubSpot
            self.client.crm.contacts.basic_api.update(
                contact_id=lead_id, simple_public_object_input=simple_public_object_input
            )
            return {"lead_id": lead_id, "updated_fields": updates}
        except ApiException as e:
            print(f"Error updating HubSpot record: {e}")
            return None

    def update_records_batch(self, leads):
        """
        Updates multiple records in HubSpot based on a list of Lead objects.

        Args:
            leads (List[Lead]): A list of Lead objects containing the updates.

        Returns:
            List[dict]: A list of updated record details.
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
